import galprime
import numpy as np
import os

from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.convolution import Gaussian2DKernel

from astropy.visualization import ZScaleInterval

from numpy.random import randint
from scipy.signal import convolve2d

import galprime

from pebble import ProcessPool
from concurrent.futures import TimeoutError

class GalPrimeError(Exception):
    pass


class GPrime():
    """ Class to create and run GalPrime simulations """
    
    def __init__(self, config=None, psfs=None, backgrounds=None, mag_kde=None):

        if config is None:
            self.config = galprime.default_config_params()
        elif type(config) == str:
            self.config = galprime.load_config_file(config)
        elif type(config) == dict:
            self.config = config
        else:
            raise GalPrimeError("Uncertain format for config file. File needs to be dict object or str filename.")
            sys.exit(1)
        
        self.binned_objects = None
        self.psfs = psfs
        self.backgrounds = backgrounds
        self.mag_kde = mag_kde

    def load_bins(self):
        self.binned_objects = galprime.bin_catalog(self.config)
    
    
    def pipeline(self, max_bins=None, mag_kde=None, process_method=None,
                progress_bar=False, debug=False, 
                 table_names=["ID","IMG", "X", "Y", "RA", "DEC", "MAGS", "R50S", "NS", "ELLIPS", "MASS_MED",
                              "ZPHOT", "sfProb", "I_R50", "PA", "R50_PIX", "BG_MEAN", "BG_MED", "BG_STD",
                              "NSEG_BGA", "CENT_BGA", "N_MASKED_BGA", "P_MASKED_BGA", "NSEG_BGSUB", "CENT_BGSUB", 
                              "N_MASKED_BGSUB", "P_MASKED_BGSUB"]):
        
        # Bin out catalog based on the catalog in the configuration file
        binned_objects = galprime.bin_catalog(self.config)
        max_bins = len(binned_objects.bins) if max_bins is None else max_bins
        
        verbose = self.config["VERBOSE"]

        if not os.path.isdir(self.config["OUT_DIR"]):
            os.mkdir(self.config["OUT_DIR"])
        
        # Run through bins and process using the method
        for i in range(max_bins):
            current_bin = binned_objects.bins[i]
            
            columns = current_bin.columns()
            
            # Generate the object KDE that will be used by this bin
            kde = galprime.object_kde(columns)
            
            # Create our container object (this is what will be multithreaded) ###
            bg_index = randint(len(self.backgrounds.cutouts))
            
            job_list, job_results = [], []
            # Set up the job pool
            print("Generating", self.config["N_MODELS"], "models for bin:", current_bin.bin_params)
            with ProcessPool(max_workers=self.config["CORES"]) as pool:
                for i in range(self.config["N_MODELS"]):
                    job_list.append(pool.schedule(process_method,
                                                args=(self, current_bin, kde),
                                                timeout=self.config["TIME_LIMIT"]))
            # Now get all the results
            for i, job in enumerate(job_list):
                try:
                    job_results.append(job.result())
                except Exception as error:
                    print(error.args, i)
            
            print(len(job_results))



class GalPrimeContainer:
    
    def __init__(self, config=None, kde=None, mag_kde=None, background=None, psf=None,
                 model_cutout=None, background_cutout=None, bg_model=None,
                 bgadded_masked=None, bgsub_cutout=None, bgsub_masked=None, 
                 model_profile=None, bgadded_profile=None, bgsub_profile=None,
                 metadata=None):
        
        if config == None:
            self.config = galprime.default_config_params()
        else:
            self.config = config
        
        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata
            
        # Generate Container ID
        self.metadata["ID"] = np.random.randint(1e15,1e16)
        
        self.kde = kde
        self.mag_kde = mag_kde
        self.background = background
        
        # Models without masking
        self.model = model_cutout
        self.convolved_model = None
        self.background_cutout = background_cutout
        self.bgsub_cutout = bgsub_cutout
        self.psf = psf
        
        # Background-added cutouts after masking
        self.bgadded_masked = bgadded_masked
        self.bgsub_masked = bgsub_masked
        self.bg_model = bg_model
        
        # Extracted profiles
        self.model_profile = model_profile
        self.bgadded_profile = bgadded_profile
        self.bgsub_profile = bgsub_profile
    
    # Functions to run ########################################################################
    def generate_model(self):
        if self.config["DEBUG"]:
            print("Generating Sersic model cutout of size", self.config["EXTRACTION_SIZE"])    
        self.model, model_params = galprime.model_from_kde(self.kde, self.config, self.mag_kde, 
                                                           names=self.metadata["NAMES"])
        self.metadata.update(model_params)
        
        
    def get_background(self):
        # Get background and convolve model with associated Best PSF
        
        # self.psf = galprime.get_closest_psf(psfs, self.metadata["RA"], self.metadata["DEC"])
                
        # Convolve model with the PSF, and add the model to the background
        self.convolved_model = convolve2d(self.model, self.psf, mode='same')
        self.bgadded_cutout = self.convolved_model + self.background_cutout
        
        bg_stats = galprime.estimate_background_sigclip(self.bgadded_cutout, config=self.config)
        self.metadata["BG_MEAN"], self.metadata["BG_MED"], self.metadata["BG_STD"] = bg_stats
    
    def subtract_background(self):
        if self.config["DEBUG"]:
            print("Subtracting the background from the bgadded cutout")
        sm = galprime.SourceMask(self.convolved_model + self.background_cutout) 
        mask = sm.multiple(filter_fwhm=[1,3,5], tophat_size=[4,2,1])
        self.bgmask = mask
        
        bg_2D = galprime.background_2D(self.bgadded_cutout, self.bgmask, self.config["BOX_SIZE"], filter_size=self.config["FILTER_SIZE"])
        self.bg_model = bg_2D.background
        
    def mask_cutouts(self):
        if self.config["DEBUG"]:
            print("Masking all profiles")
        # Apply masking to both bgadded and bgsub, add these to the container, and update the metadata
        bgadded_masked = galprime.MaskedCutout(cutout=self.bgadded_cutout, config=self.config)
        bgadded_masked.mask_cutout()
        self.bgadded_masked = bgadded_masked.masked_cutout
        self.metadata.update(galprime.dict_extend(bgadded_masked.mask_info, extension="_BGA"))

        bgsub_masked = galprime.MaskedCutout(cutout=self.bgadded_cutout - self.bg_model, config=self.config)
        bgsub_masked.mask_cutout()
        self.metadata.update(galprime.dict_extend(bgsub_masked.mask_info, extension="_BGSUB"))            
        self.bgsub_masked = bgsub_masked.masked_cutout

            
    def extract_profiles(self):
        if self.config["DEBUG"]:
            print("Extracting all profiles")
        self.model_profile = galprime.isophote_fitting(self.convolved_model, config=self.config)
        self.bgadded_profile = galprime.isophote_fitting(self.bgadded_masked, config=self.config)
        self.bgsub_profile = galprime.isophote_fitting(self.bgsub_masked, config=self.config)
            
            
    def save_data(self):
        if self.config["DEBUG"]:
            print("Saving data")
    
    def plot_data(self, filename="out.png"):
        fig, ax = plt.subplots(2,5, facecolor="white")
        fig.set_figheight(5)
        fig.set_figwidth(12)
        
        scale = ZScaleInterval(contrast=0.5).get_limits(self.bgadded_cutout)
        
        ax[0][0].imshow(self.model, origin='lower', vmin=scale[0], vmax=scale[1], cmap="Greys")
        ax[0][1].imshow(self.convolved_model, origin='lower', vmin=scale[0], vmax=scale[1], cmap="Greys")
        ax[0][2].imshow(self.psf, origin='lower', cmap="Greys")
        ax[0][3].imshow(self.background_cutout, origin='lower', vmin=scale[0], vmax=scale[1], cmap="Greys")
        ax[0][4].imshow(self.convolved_model + self.background_cutout, origin='lower', vmin=scale[0], 
        vmax=scale[1], cmap="Greys")
        
        ax[1][0].imshow(self.bg_model, origin="lower", vmin=scale[0], vmax=scale[1], cmap="Greys")
        ax[1][1].imshow(self.bgmask, origin='lower', cmap="Greys")
        ax[1][2].imshow(self.bgadded_masked, origin='lower', vmin=scale[0], vmax=scale[1], cmap="Greys")
        ax[1][3].imshow(self.bgsub_masked, origin='lower', vmin=scale[0], vmax=scale[1], cmap="Greys")
        
        
        ax[0][0].set_title("Model")
        ax[0][1].set_title("Convolved Model")
        ax[0][2].set_title("PSF")
        ax[0][3].set_title("Background Cutout")
        ax[0][4].set_title("Combined Cutout")
        
        ax[1][0].set_title("Model Background")
        ax[1][1].set_title("Background Mask")
        ax[1][2].set_title("Masked BGAdded")
        ax[1][3].set_title("Masked BG-Subbed")
        ax[1][4].set_title("Profiles: Flux vs " + r'$R^{1/4}$')
        
        bare_prof = self.model_profile
        bgadded_prof = self.bgadded_profile
        bgsub_prof = self.bgsub_profile
        
        
        ax[1][4].plot(bare_prof.sma ** (1/4), np.log10(bare_prof.intens), color="red")
        ax[1][4].plot(bgadded_prof.sma ** (1/4), np.log10(bgadded_prof.intens), color="blue")
        ax[1][4].plot(bgsub_prof.sma ** (1/4), np.log10(bgsub_prof.intens), color="gold")

        for j in range(5):
            for i in range(2):
                ax[i][j].set_xticks([])
                ax[i][j].set_yticks([])
        
        ax[1][4].set_xticks(np.arange(0, np.max(bare_prof.sma ** (1/4))))
        
        plt.suptitle("ID: " + str(self.metadata["ID"]))
        plt.tight_layout()
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename, dpi=150)
        
    
    def save_outputs(self, filename="GalPrimeContainer.fits", overwrite=True):
        print("Saving output")
        out_HDUList = fits.HDUList()
        head = fits.Header()
        
        for n in self.metadata:
            val = self.metadata[n]
            if type(val) == list:
                continue
            head[n] = self.metadata[n]
        
        out_HDUList.append(fits.PrimaryHDU(header=head))
        out_HDUList.append(fits.ImageHDU(data=self.convolved_model, name="MODEL"))
        out_HDUList.append(fits.ImageHDU(data=self.bgadded_cutout, name="BGA_IMG"))
        out_HDUList.append(fits.ImageHDU(data=self.bgsub_cutout, name="BGS_IMG"))
        out_HDUList.append(fits.ImageHDU(data=self.bgadded_masked, name="BGAMASKED"))
        out_HDUList.append(fits.ImageHDU(data=self.bgsub_masked, name="BGSMASKED"))
        out_HDUList.append(fits.ImageHDU(data=self.bg_model, name="BGMODEL"))
        out_HDUList.append(fits.BinTableHDU(data=galprime.table_from_isolist(self.model_profile), name="MOD_PROF"))
        out_HDUList.append(fits.BinTableHDU(data=galprime.table_from_isolist(self.bgadded_profile), name="BGA_PROF"))
        out_HDUList.append(fits.BinTableHDU(data=galprime.table_from_isolist(self.bgsub_profile), name="BGS_PROF"))
       
        print(len(out_HDUList), type(out_HDUList))
        
        out_HDUList.writeto(filename, overwrite=overwrite)
        

    def process_object(self, plot=False):
        self.generate_model()
        self.get_background()
        self.subtract_background()
        self.mask_cutouts()
        self.extract_profiles()
        self.save_data()
        
        if plot:
            outdir = self.config["OUT_DIR"] + "pngs/"
            if not os.path.isdir(outdir):
                os.mkdir(outdir)
            self.plot_data(filename=outdir + "obj_" + str(self.metadata["ID"]) + ".png")


def gprime_single(gprime_obj, current_bin, kde):
    metadata = {}
    metadata["NAMES"] = current_bin.object_column_names
    
    bg_index = randint(len(gprime_obj.backgrounds.cutouts))
    metadata["BG_INDEX"] = bg_index
    
    metadata.update(gprime_obj.backgrounds.cutout_data[bg_index])

    # Get the best PSF is the user has supplied PSFs to the pipeline
    # Otherwise, just use a simple Gaussian2D kernel from astropy
    if gprime_obj.psfs is None:
        psf = Gaussian2DKernel(x_stddev=1.5, y_stddev=1.5)
    else:
        psf = galprime.get_closest_psf(gprime_obj.psfs, metadata["RA"], metadata["DEC"])

    # Generate our container
    container = GalPrimeContainer(config=gprime_obj.config, kde=kde, psf=psf,
                                    background_cutout=gprime_obj.backgrounds.cutouts[bg_index], 
                                    metadata=metadata)
    container.process_object(plot=True)
    return container
