from typing import Any, Dict

from pete_tpl import dll
from pete_tpl.exception import EngineCreateException, EngineDestroyException, RenderingException
from pete_tpl.c_type_conversion import python_dict_to_c_array
from pete_tpl.typedefs import PETETPL_RESULT_OK

import ctypes


class PeteTpl:
    def __init__(self):
        self.dll_handle = None  # pre-defined, as it will be needed in destructor method

        dll.init()
        self.lib = dll.get_lib()
        result = self.lib.petetpl_new_engine()
        if result < 0:
            raise EngineCreateException(result)
        self.dll_handle = result

    def __del__(self):
        if self.dll_handle is not None:
            result = self.lib.petetpl_destroy_engine(self.dll_handle)
            if result != PETETPL_RESULT_OK:
                raise EngineDestroyException(self.dll_handle, result)

    def render(self, template: str, parameters: Dict[str, Any] = None) -> str:
        if parameters is None:
            parameters = {}

        (c_params_c, c_params_v) = python_dict_to_c_array(parameters)
        result = self.lib.petetpl_render(self.dll_handle, ctypes.c_char_p(template.encode('utf-8')), c_params_c, c_params_v)

        exception = None if result.is_succeeded else RenderingException(result)
        output = result.output.decode('utf-8')
        self.lib.petetpl_free_render_result(result)

        if exception:
            raise exception

        return output
