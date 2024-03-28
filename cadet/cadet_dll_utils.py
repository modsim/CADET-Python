import ctypes
import numpy

def null(*args):
    pass

if 0:
    log_print = print
else:
    log_print = null


def param_provider_get_double(reader, name, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]
        try:
            float_val = float(o)
        except TypeError:
            float_val = float(o[0])

        val[0] = ctypes.c_double(float_val)

        log_print('GET scalar [double] {}: {}'.format(n, float(val[0])))
        return 0

    return -1


def param_provider_get_int(reader, name, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]
        try:
            int_val = int(o)
        except TypeError:
            int_val = int(o[0])

        val[0] = ctypes.c_int(int_val)

        log_print('GET scalar [int] {}: {}'.format(n, int(val[0])))
        return 0

    return -1


def param_provider_get_bool(reader, name, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]

        try:
            int_val = int(o)
        except TypeError:
            int_val = int(o[0])

        val[0] = ctypes.c_uint8(int_val)

        log_print('GET scalar [bool] {}: {}'.format(n, bool(val[0])))
        return 0

    return -1


def param_provider_get_string(reader, name, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]

        #we have one of array of strings, array of bytestrings, bytestring or string or something convertable to one of these
        if hasattr(o, 'encode'):
            bytes_val = o.encode('utf-8')
        elif hasattr(o, 'decode'):
            bytes_val = o
        elif hasattr(o[0], 'encode'):
            bytes_val = o[0].encode('utf-8')
        elif hasattr(o[0], 'decode'):
            bytes_val = o[0]

        reader.buffer = bytes_val
        val[0] = ctypes.cast(reader.buffer, ctypes.c_char_p)

        return 0

    return -1


def param_provider_get_double_array(reader, name, n_elem, val):
    n = name.decode('utf-8')
    c = reader.current()

    if (n in c):
        o = c[n]
        if isinstance(o, list):
            o = numpy.ascontiguousarray(o)
        if (not isinstance(o, numpy.ndarray)) or (o.dtype != numpy.double) or (not o.flags.c_contiguous):
            return -1

        n_elem[0] = ctypes.c_int(o.size)
        val[0] = o.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        log_print('GET array [double] {}: {}'.format(n, o))
        return 0

    return -1


def param_provider_get_int_array(reader, name, n_elem, val):
    n = name.decode('utf-8')
    c = reader.current()

    if (n in c):
        o = c[n]
        if isinstance(o, list):
            o = numpy.ascontiguousarray(o)
        if (not isinstance(o, numpy.ndarray)) or (o.dtype != int) or (not o.flags.c_contiguous):
            return -1

        n_elem[0] = ctypes.c_int(o.size)
        val[0] = o.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        log_print('GET array [int] {}: {}'.format(n, o))
        return 0

    return -1


def param_provider_get_double_array_item(reader, name, index, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]

        try:
            float_val = float(o)
        except TypeError:
            float_val = float(o[index])

        val[0] = ctypes.c_double(float_val)
        log_print('GET array [double] ({}) {}: {}'.format(index, n, val[0]))
        return 0

    return -1


def param_provider_get_int_array_item(reader, name, index, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]

        try:
            int_val = int(o)
        except TypeError:
            int_val = int(o[index])

        val[0] = ctypes.c_int(int_val)
        log_print('GET array [int] ({}) {}: {}'.format(index, n, val[0]))
        return 0

    return -1


def param_provider_get_bool_array_item(reader, name, index, val):
    n = name.decode('utf-8')
    c = reader.current()

    if n in c:
        o = c[n]

        try:
            int_val = int(o)
        except TypeError:
            int_val = int(o[index])

        val[0] = ctypes.c_uint8(int_val)
        log_print('GET array [bool] ({}) {}: {}'.format(index, n, bool(val[0])))
        return 0

    return -1


def param_provider_get_string_array_item(reader, name, index, val):
    name = name.decode('utf-8')
    current_reader = reader.current()

    if name in current_reader:
        str_value = current_reader[name]
        if isinstance(str_value, bytes):
            bytes_val = str_value
        else:
            bytes_val = str_value[index]

        reader.buffer = bytes_val
        val[0] = ctypes.cast(reader.buffer, ctypes.c_char_p)
        log_print(f"GET array [string] ({index}) {name}: {reader.buffer.decode('utf-8')}")

        return 0

    return -1


def param_provider_exists(reader, name):
    n = name.decode('utf-8')
    c = reader.current()

    log_print('EXISTS {}: {}'.format(n, n in c))

    if n in c:
        return 1

    return 0


def param_provider_is_array(reader, name, res):
    n = name.decode('utf-8')
    c = reader.current()

    if n not in c:
        return -1

    o = c[n]
    res[0] = ctypes.c_uint8(0)
    if isinstance(o, list):
        res[0] = ctypes.c_uint8(1)
    elif isinstance(o, numpy.ndarray):
        res[0] = ctypes.c_uint8(1)

    log_print('ISARRAY {}: {}'.format(n, bool(res[0])))

    return 0


def param_provider_num_elements(reader, name):
    n = name.decode('utf-8')
    c = reader.current()

    if n not in c:
        return -1

    o = c[n]
    if isinstance(o, list):
        log_print('NUMELEMENTS {}: {}'.format(n, len(o)))
        return len(o)
    elif isinstance(o, numpy.ndarray):
        log_print('NUMELEMENTS {}: {}'.format(n, o.size))
        return o.size

    log_print('NUMELEMENTS {}: {}'.format(n, 1))
    return 1

def param_provider_push_scope(reader, name):
	n = name.decode('utf-8')

	if reader.push_scope(n):
		return 0
	else:
		return -1


def param_provider_pop_scope(reader):
	reader.pop_scope()
	return 0
