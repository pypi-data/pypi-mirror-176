import ctypes

from pete_tpl.typedefs import PeteTplRenderResult


class InitException(Exception):
    def __init__(self, code: ctypes.c_int, msg=None, *args, **kwargs):
        if msg is None:
            msg = f'PETE: Failed to initialize the library. Code: {code}'
        super().__init__(msg, *args, **kwargs)
        self.code = code


class EngineCreateException(Exception):
    def __init__(self, code: ctypes.c_int, msg=None, *args, **kwargs):
        if msg is None:
            msg = f'PETE: Failed to create an engine. Code: {code}'
        super().__init__(msg, *args, **kwargs)
        self.code = code


class EngineDestroyException(Exception):
    def __init__(self, handle: ctypes.c_int, code: ctypes.c_int, msg=None, *args, **kwargs):
        if msg is None:
            msg = f'PETE: Failed to destroy an engine with handle {handle}. Code: {code}'
        super().__init__(msg, *args, **kwargs)
        self.code = code
        self.handle = handle


class NotInitializedException(Exception):
    def __init__(self, msg='PETE is not initialized', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class RenderingException(Exception):
    def __init__(self, result: PeteTplRenderResult, msg=None, *args, **kwargs):
        self.result = result
        if msg is None:
            msg = f"An error occurred. Code: {result.code}, message: {result.output}"
        super().__init__(msg, *args, **kwargs)
