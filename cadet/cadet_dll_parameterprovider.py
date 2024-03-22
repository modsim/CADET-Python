import ctypes

import addict

import cadet.cadet_dll_utils as utils

c_cadet_result = ctypes.c_int

array_double = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

point_int = ctypes.POINTER(ctypes.c_int)


def null(*args):
    pass


if 0:
    log_print = print
else:
    log_print = null


class NestedDictReader:

    def __init__(self, data):
        self._root = data
        self._cursor = []
        self._cursor.append(data)
        self.buffer = None

    def push_scope(self, scope):
        if scope in self._cursor[-1]:
            log_print('Entering scope {}'.format(scope))
            self._cursor.append(self._cursor[-1][scope])
            return True

        return False

    def pop_scope(self):
        self._cursor.pop()
        log_print('Exiting scope')

    def current(self):
        return self._cursor[-1]


def recursively_convert_dict(data):
    ans = addict.Dict()
    for key_original, item in data.items():
        if isinstance(item, dict):
            ans[key_original] = recursively_convert_dict(item)
        else:
            key = str.upper(key_original)
            ans[key] = item
    return ans


class PARAMETERPROVIDER(ctypes.Structure):
    """Implemented the CADET Parameter Provider interface which allows 
    querying python for the necessary parameters for a CADET simulation
    
    _fields_ is a list of function names and signatures exposed by the
    capi Parameter Provider interface
    https://docs.python.org/3/library/ctypes.html
    https://github.com/modsim/CADET/blob/master/src/libcadet/api/CAPIv1.cpp"""

    def __init__(self, simulation):
        sim_input = recursively_convert_dict(simulation)

        self.userData = NestedDictReader(sim_input)

        # figure out how to add this to the class
        self.getDouble = self._fields_[1][1](utils.param_provider_get_double)
        self.getInt = self._fields_[2][1](utils.param_provider_get_int)
        self.getBool = self._fields_[3][1](utils.param_provider_get_bool)
        self.getString = self._fields_[4][1](utils.param_provider_get_string)

        self.getDoubleArray = self._fields_[5][1](utils.param_provider_get_double_array)
        self.getIntArray = self._fields_[6][1](utils.param_provider_get_int_array)
        self.getBoolArray = ctypes.cast(None, self._fields_[7][1])
        self.getStringArray = ctypes.cast(None, self._fields_[8][1])

        self.getDoubleArrayItem = self._fields_[9][1](utils.param_provider_get_double_array_item)
        self.getIntArrayItem = self._fields_[10][1](utils.param_provider_get_int_array_item)
        self.getBoolArrayItem = self._fields_[11][1](utils.param_provider_get_bool_array_item)
        self.getStringArrayItem = self._fields_[12][1](utils.param_provider_get_string_array_item)

        self.exists = self._fields_[13][1](utils.param_provider_exists)
        self.isArray = self._fields_[14][1](utils.param_provider_is_array)
        self.numElements = self._fields_[15][1](utils.param_provider_num_elements)
        self.pushScope = self._fields_[16][1](utils.param_provider_push_scope)
        self.popScope = self._fields_[17][1](utils.param_provider_pop_scope)

    _fields_ = [
        (
            'userData',
            ctypes.py_object
        ),
        (
            'getDouble',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double))
        ),
        (
            'getInt',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, point_int)
        ),
        (
            'getBool',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8))
        ),
        (
            'getString',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p))
        ),
        (
            'getDoubleArray',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, point_int, array_double)
        ),
        (
            'getIntArray',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, point_int, ctypes.POINTER(point_int))
        ),
        (
            'getBoolArray',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, point_int,
                             ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)))
        ),
        (
            'getStringArray',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, point_int,
                             ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)))
        ),
        (
            'getDoubleArrayItem',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.c_int,
                             ctypes.POINTER(ctypes.c_double))
        ),
        (
            'getIntArrayItem',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.c_int, point_int)
        ),
        (
            'getBoolArrayItem',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.c_int,
                             ctypes.POINTER(ctypes.c_uint8))
        ),
        (
            'getStringArrayItem',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.c_int,
                             ctypes.POINTER(ctypes.c_char_p))
        ),
        (
            'exists',
            ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_char_p)
        ),
        (
            'isArray',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8))
        ),
        (
            'numElements',
            ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_char_p)
        ),
        (
            'pushScope',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object, ctypes.c_char_p)
        ),
        (
            'popScope',
            ctypes.CFUNCTYPE(c_cadet_result, ctypes.py_object)
        ),
    ]

    # these don't work right now but work when places on an instance
    # getDouble = _fields_[1][1](utils.param_provider_get_double)
    # getInt = _fields_[2][1](utils.param_provider_get_int)
    # getBool = _fields_[3][1](utils.param_provider_get_bool)
    # getString = _fields_[4][1](utils.param_provider_get_string)

    # getDoubleArray = _fields_[5][1](utils.param_provider_get_double_array)
    # getIntArray = _fields_[6][1](utils.param_provider_get_int_array)
    # getBoolArray = ctypes.cast(None, _fields_[7][1])
    # getStringArray = ctypes.cast(None, _fields_[8][1])

    # getDoubleArrayItem = _fields_[9][1](utils.param_provider_get_double_array_item)
    # getIntArrayItem = _fields_[10][1](utils.param_provider_get_int_array_item)
    # getBoolArrayItem = _fields_[11][1](utils.param_provider_get_bool_array_item)
    # getStringArrayItem = _fields_[12][1](utils.param_provider_get_string_array_item)

    # exists = _fields_[13][1](utils.param_provider_exists)
    # isArray = _fields_[14][1](utils.param_provider_is_array)
    # numElements = _fields_[15][1](utils.param_provider_num_elements)
    # pushScope = _fields_[16][1](utils.param_provider_push_scope)
    # popScope = _fields_[17][1](utils.param_provider_pop_scope)
