from .common import *
# from .prod import *


# # local development environment overrides of production settings
# try:
#     from .dev import *
# except ImportError:
#     pass

try:
    from .dev import *
    live = False
except:
    live = True

if live:
    from .prod import *
