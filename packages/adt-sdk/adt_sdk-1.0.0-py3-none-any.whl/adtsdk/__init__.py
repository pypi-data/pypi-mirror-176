import pkg_resources

from adtsdk.datasource import DataFormat, DataSources
from adtsdk.upload import Uploader

try:
    __version__ = pkg_resources.get_distribution("adt").version
except pkg_resources.DistributionNotFound:
    __version__ = "dev"
