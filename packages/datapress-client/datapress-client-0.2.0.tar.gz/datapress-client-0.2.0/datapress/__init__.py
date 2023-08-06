"""
datapress_client

DataPress API client and utilities.
"""

from .__version__ import __version__ as version
print('Loading datapress_client version: ' + version)

from .dataset import get_dataset
from . import geo
from . import extract
from . import nomis
from . import api
from . import dataset
