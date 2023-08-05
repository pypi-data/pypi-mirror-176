import ctypes
from typing import Any, Dict, Tuple

from pete_tpl import typedefs


def python_dict_to_c_array(params: Dict[str, Any]) -> Tuple[ctypes.c_uint, ctypes.POINTER(typedefs.PeteTplParam)]:
    """Converts a Python map into C-compatible pointer
    """
    c_args_v = []
    for param_name, param_value in params.items():
        [tag_value, val_value] = _get_value_tag_and_val(param_value)
        c_param = typedefs.PeteTplParam(name=ctypes.c_char_p(param_name.encode('utf-8')),
                                        value=typedefs.PeteTplParamValue(
                                            tag=tag_value,
                                            value=val_value))
        c_args_v.append(c_param)

    c_args_c = len(params)
    c_args_v = (typedefs.PeteTplParam * c_args_c)(*c_args_v)
    c_args_v = ctypes.cast(c_args_v, ctypes.POINTER(typedefs.PeteTplParam))

    return (c_args_c, c_args_v)


def _get_value_tag_and_val(param_value: Any) -> Tuple[ctypes.c_uint, typedefs.PeteTplParamValueContent]:
    if isinstance(param_value, list):
        c_items_v = []
        for item in param_value:
            [tag_value, val_value] = _get_value_tag_and_val(item)
            c_items_v.append(typedefs.PeteTplParamValue(tag=tag_value, value=val_value))

        c_items_c = len(c_items_v)
        c_items_v = (typedefs.PeteTplParamValue * c_items_c)(*c_items_v)
        c_items_v = ctypes.cast(c_items_v, ctypes.POINTER(typedefs.PeteTplParamValue))

        return [typedefs.PETETPL_PARAMVALUE_TAG_ARRAY,
                typedefs.PeteTplParamValueContent(
                    array_=typedefs.PeteTplArrayBody(
                        _0=c_items_c,
                        _1=c_items_v
                    )
                )]

    if isinstance(param_value, bool):
        return [typedefs.PETETPL_PARAMVALUE_TAG_BOOLEAN,
                typedefs.PeteTplParamValueContent(
                    bool_=ctypes.c_uint32(param_value)
                )]
    elif isinstance(param_value, float):
        return [typedefs.PETETPL_PARAMVALUE_TAG_FLOAT,
                typedefs.PeteTplParamValueContent(
                    float_=ctypes.c_float(param_value)
                )]
    elif isinstance(param_value, int):
        return [typedefs.PETETPL_PARAMVALUE_TAG_INT,
                typedefs.PeteTplParamValueContent(
                    int_=ctypes.c_int(param_value)
                )]
    elif isinstance(param_value, str):
        return [typedefs.PETETPL_PARAMVALUE_TAG_STRING,
                typedefs.PeteTplParamValueContent(
                    string=ctypes.c_char_p(param_value.encode('utf-8'))
                )]
    if isinstance(param_value, dict):
        [c, v] = python_dict_to_c_array(param_value)
        return [typedefs.PETETPL_PARAMVALUE_TAG_STRUCT,
                typedefs.PeteTplParamValueContent(
                    struct_=typedefs.PeteTplStructBody(
                        _0=c,
                        _1=v,
                    )
                )]

    raise TypeError(f"Unknown type of {param_value}")
