from .common import *
from .prod import *


# local development environment overrides of production settings
try:
    from .dev import *
except ImportError:
    pass
