name = "Zodiax"
__version__ = "0.1"

# Import as modules
from . import test

# Import core functions from modules
from .test import *

# Add to __all__
__all__ = test.__all__