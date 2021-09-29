"""
mmic_translator
Generic MMSchema translator
"""

# Add imports here
from .models import *
from .components import *
from .mmic_translator import *

# Handle versioneer
from ._version import get_versions

versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
