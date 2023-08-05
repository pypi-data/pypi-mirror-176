
__version__ = "2.0.1"

from .backgrounds import *
from .binning import *
from .config import *
from .data import *
from .extraction import *
from .koe import *
from .masking import *
from .modelling import *
from .sims import *

# from .densities import *
# from .medians import *
# from .profiles import *

from . import plotting

def __main__():
    pass


class GalPrimeError(Exception):
    pass


