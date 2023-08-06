

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_1():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'geopolars.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        load_order_filepath = os.path.join(libs_dir, '.load-order-geopolars-0.1.0a4')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-geopolars-0.1.0a4')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    WinDLL(lib_path)


_delvewheel_init_patch_1_1_1()
del _delvewheel_init_patch_1_1_1
# end delvewheel patch

from geopolars.convert import from_arrow, from_geopandas
from geopolars.geopolars import version  # type: ignore
from geopolars.internals.geodataframe import GeoDataFrame
from geopolars.internals.geoseries import GeoSeries
from geopolars.io.file import read_file

from . import datasets  # noqa

__all__ = [
    # geopolars.io.file
    "read_file",
    # geopolars.convert
    "from_arrow",
    "from_geopandas",
    # geopolars.internals
    "GeoDataFrame",
    "GeoSeries",
]

__version__: str = version()
