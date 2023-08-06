from pkg_resources import get_distribution
from . import file0
from .folder1 import file1
from .folder2 import file2
from .folder1.subfolder1 import file3

__version__ = get_distribution('multi-folder-pkg-deps-insomniapx').version