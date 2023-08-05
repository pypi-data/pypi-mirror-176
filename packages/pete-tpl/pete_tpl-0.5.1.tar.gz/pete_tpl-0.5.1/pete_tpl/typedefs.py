from ctypes import Structure, Union, POINTER, c_char_p, c_int, c_uint, c_float

"""C-compatible type definitions"""

PETETPL_RESULT_OK = 0
PETETPL_RESULT_ERROR_NOT_INITIALIZED = -1
PETETPL_RESULT_ERROR_HANDLE_NOT_FOUND = -2
PETETPL_RESULT_ERROR_FAILED_TO_PARSE_INPUT_STRING = -3
PETETPL_RESULT_ERROR_MISC = -100

PETETPL_PARAMVALUE_TAG_ARRAY = 0
PETETPL_PARAMVALUE_TAG_BOOLEAN = 1
PETETPL_PARAMVALUE_TAG_FLOAT = 2
PETETPL_PARAMVALUE_TAG_INT = 3
PETETPL_PARAMVALUE_TAG_STRING = 4
PETETPL_PARAMVALUE_TAG_STRUCT = 5


PeteTplFnResult = c_int


class PeteTplRenderResult(Structure):
    _fields_ = [("code", PeteTplFnResult),
                ("is_succeeded", c_uint),
                ("output", c_char_p)]


class PeteTplStructBody(Structure):
    pass


class PeteTplArrayBody(Structure):
    pass


class PeteTplParamValueContent(Union):
    pass


class PeteTplParamValue(Structure):
    pass


class PeteTplParam(Structure):
    pass


PeteTplStructBody._fields_ = [("_0", c_uint), ("_1", POINTER(PeteTplParam))]

PeteTplArrayBody._fields_ = [("_0", c_uint), ("_1", POINTER(PeteTplParamValue))]

PeteTplParamValueContent._fields_ = [
                ("array_", PeteTplArrayBody),
                ("bool_", c_uint),
                ("float_", c_float),
                ("int_", c_int),
                ("string", c_char_p),
                ("struct_", PeteTplStructBody)]

PeteTplParamValue._fields_ = [("tag", c_uint),
                              ("value", PeteTplParamValueContent)]

PeteTplParam._fields_ = [("name", c_char_p),
                         ("value", PeteTplParamValue)]
