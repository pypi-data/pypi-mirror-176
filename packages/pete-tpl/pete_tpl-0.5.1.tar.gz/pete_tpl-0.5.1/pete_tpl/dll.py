import ctypes
import os
import platform

import pete_tpl
from pete_tpl import typedefs
from pete_tpl.typedefs import PeteTplParam, PeteTplRenderResult
from pete_tpl import exception

"""This module handles interaction with library (DLL/SO/...)"""

FILE_NAMES = {
    'linux': 'libpetetpl.so',
    'windows': 'petetpl.dll',
}

lib = None


def format_shared_lib_path() -> str:
    """Formats the path to library file. The library is located in module's root dir.
    Example: pete_tpl/libpetetpl.so"""
    os_name = platform.system().lower()
    filename = FILE_NAMES.get(os_name)
    if filename is None:
        raise Exception(f'Cannot determine a library file name for OS: {os_name}')
    module_dir = os.path.dirname(pete_tpl.__file__)
    lib_filename = os.path.join(module_dir, filename)
    return lib_filename


def init():
    """Loads and initialized the library"""
    global lib
    if lib is not None:
        return
    lib = ctypes.cdll.LoadLibrary(format_shared_lib_path())

    lib.petetpl_new_engine.restype = ctypes.c_int

    lib.petetpl_render.restype = PeteTplRenderResult
    lib.petetpl_render.argtypes = [ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.POINTER(PeteTplParam)]

    lib.petetpl_free_render_result.argtypes = [PeteTplRenderResult]

    lib.petetpl_destroy_engine.argtypes = [ctypes.c_uint]
    lib.petetpl_free.restype = ctypes.c_int

    init_result = lib.petetpl_init()
    if init_result != typedefs.PETETPL_RESULT_OK:
        raise exception.InitException(init_result)


def get_lib() -> ctypes.CDLL:
    """Returns a handle of the library"""
    if lib is None:
        raise exception.NotInitializedException()
    return lib
