from datetime import datetime
from libdlf import hankel
from libdlf import fourier
try:
    from libdlf.version import version as __version__
except ImportError:
    __version__ = 'unknown-'+datetime.today().strftime('%Y%m%d')
