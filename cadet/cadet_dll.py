import ctypes
import numpy
import addict
import cadet.cadet_dll_parameterprovider as cadet_dll_parameterprovider


def log_handler(file, func, line, level, level_name, message):
    log_print('{} ({}:{:d}) {}'.format(level_name.decode('utf-8') , func.decode('utf-8') , line, message.decode('utf-8') ))

def _no_log_output(*args):
    pass

if 0:
    log_print = print
else:
    log_print = _no_log_output

# Some common types
CadetDriver = ctypes.c_void_p
array_double = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
point_int = ctypes.POINTER(ctypes.c_int)

# Values of cdtResult
# TODO: Convert to lookup table to improve error messages below.
c_cadet_result = ctypes.c_int
_CDT_OK = 0
_CDT_ERROR = -1
_CDT_ERROR_INVALID_INPUTS = -2
_CDT_DATA_NOT_STORED = -3


class CADETAPIV010000_DATA():
    """
    Definition of CADET-C-API v1.0

    signatures : dict with signatures of exported API functions. (See CADET/include/cadet/cadet.h)
    lookup_prototype : ctypes for common parameters
    lookup_output_argument_type : ctypes for API output parameters (e.g., double* time or double** data)

    """

    # Order is important, has to match the cdtAPIv010000 struct of the C-API
    signatures = {}
    signatures['createDriver'] = ('drv',)
    signatures['deleteDriver'] = (None, 'drv')
    signatures['runSimulation'] = ('return', 'drv', 'parameterProvider')

    signatures['getNumParTypes'] = ('return', 'drv', 'unitOpId', 'nParTypes')
    signatures['getNumSensitivities'] = ('return', 'drv', 'nSens')

    signatures['getSolutionInlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSolutionOutlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSolutionBulk'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp')
    signatures['getSolutionParticle'] = ('return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nComp')
    signatures['getSolutionSolid'] = ('return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nBound')
    signatures['getSolutionFlux'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParTypes', 'nComp')
    signatures['getSolutionVolume'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime')

    signatures['getSolutionDerivativeInlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSolutionDerivativeOutlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSolutionDerivativeBulk'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp')
    signatures['getSolutionDerivativeParticle'] = ('return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nComp')
    signatures['getSolutionDerivativeSolid'] = ('return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nBound')
    signatures['getSolutionDerivativeFlux'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParTypes', 'nComp')
    signatures['getSolutionDerivativeVolume'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime')

    signatures['getSensitivityInlet'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSensitivityOutlet'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSensitivityBulk'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp')
    signatures['getSensitivityParticle'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nComp')
    signatures['getSensitivitySolid'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nBound')
    signatures['getSensitivityFlux'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParTypes', 'nComp')
    signatures['getSensitivityVolume'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime')

    signatures['getSensitivityDerivativeInlet'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSensitivityDerivativeOutlet'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nPort', 'nComp')
    signatures['getSensitivityDerivativeBulk'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp')
    signatures['getSensitivityDerivativeParticle'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nComp')
    signatures['getSensitivityDerivativeSolid'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'parType', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParShells', 'nBound')
    signatures['getSensitivityDerivativeFlux'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nParTypes', 'nComp')
    signatures['getSensitivityDerivativeVolume'] = ('return', 'drv', 'unitOpId', 'sensIdx', 'time', 'data', 'nTime')

    signatures['getLastState'] = ('return', 'drv', 'state', 'nStates')
    signatures['getLastStateTimeDerivative'] = ('return', 'drv', 'state', 'nStates')
    signatures['getLastUnitState'] = ('return', 'drv', 'unitOpId', 'state', 'nStates')
    signatures['getLastUnitStateTimeDerivative'] = ('return', 'drv', 'unitOpId', 'state', 'nStates')
    signatures['getLastSensitivityState'] = ('return', 'drv', 'sensIdx', 'state', 'nStates')
    signatures['getLastSensitivityStateTimeDerivative'] = ('return', 'drv', 'sensIdx', 'state', 'nStates')
    signatures['getLastSensitivityUnitState'] = ('return', 'drv', 'sensIdx', 'unitOpId', 'state', 'nStates')
    signatures['getLastSensitivityUnitStateTimeDerivative'] = ('return', 'drv', 'sensIdx', 'unitOpId', 'state', 'nStates')

    signatures['getPrimaryCoordinates'] = ('return', 'drv', 'unitOpId', 'coords', 'nCoords')
    signatures['getSecondaryCoordinates'] = ('return', 'drv', 'unitOpId', 'coords', 'nCoords')
    signatures['getParticleCoordinates'] = ('return', 'drv', 'unitOpId', 'parType', 'coords', 'nCoords')

    signatures['getSolutionTimes'] = ('return', 'drv', 'time', 'nTime')

    lookup_prototype = {
        'return': c_cadet_result,
        'drv': CadetDriver,
        'unitOpId': ctypes.c_int,
        'sensIdx': ctypes.c_int,
        'parType': ctypes.c_int,
        'time': array_double,
        'data': array_double,
        'coords': array_double,
        'nTime': point_int,
        'nCoords': point_int,
        'nPort': point_int,
        'nAxialCells': point_int,
        'nRadialCells': point_int,
        'nParTypes': point_int,
        'nSens': point_int,
        'nParShells': point_int,
        'nComp': point_int,
        'nBound': point_int,
        'state': array_double,
        'nStates': point_int,
        None: None,
        'parameterProvider': ctypes.POINTER(cadet_dll_parameterprovider.PARAMETERPROVIDER),
    }

    lookup_output_argument_type = {
        'time': ctypes.POINTER(ctypes.c_double),
        'nTime': ctypes.c_int,
        'data': ctypes.POINTER(ctypes.c_double),
        'nPort': ctypes.c_int,
        'nAxialCells': ctypes.c_int,
        'nRadialCells': ctypes.c_int,
        'nParTypes': ctypes.c_int,
        'nSens': ctypes.c_int,
        'nParShells': ctypes.c_int,
        'nComp': ctypes.c_int,
        'nBound': ctypes.c_int,
        'state': ctypes.POINTER(ctypes.c_double),
        'nStates': ctypes.c_int,
        'coords': ctypes.POINTER(ctypes.c_double),
        'nCoords': ctypes.c_int,
    }


def _setup_api():
    """list: Tuples with function names and ctype functions"""
    _fields_ = []

    for key, value in CADETAPIV010000_DATA.signatures.items():
        args = tuple(CADETAPIV010000_DATA.lookup_prototype[key] for key in value)
        _fields_.append( (key, ctypes.CFUNCTYPE(*args)) )

    return _fields_


class CADETAPIV010000(ctypes.Structure):
    """Mimic cdtAPIv010000 struct of CADET C-API in ctypes"""
    _fields_ = _setup_api()


class SimulationResult:

    def __init__(self, api: CADETAPIV010000, driver: CadetDriver):
        self._api = api
        self._driver = driver

    def _load_data(
            self,
            get_solution_str: str,
            unitOpId: int | None = None,
            sensIdx: int = None,
            parType: int = None):

        get_solution = getattr(self._api, get_solution_str)

        # Collect actual values
        call_args = []
        call_outputs = {}

        # Construct API call function arguments
        for key in CADETAPIV010000_DATA.signatures[get_solution_str]:
            if key == 'return':
                # Skip, this is the actual return value of the API function
                continue
            elif key == 'drv':
                call_args.append(self._driver)
            elif key == 'unitOpId' and unitOpId is not None:
                call_args.append(unitOpId)
            elif key == 'sensIdx':
                call_args.append(sensIdx)
            elif key == 'parType':
                call_args.append(parType)
            else:
                _obj = CADETAPIV010000_DATA.lookup_output_argument_type[key]()
                call_outputs[key] = _obj
                call_args.append(ctypes.byref(_obj))

        result = get_solution(*call_args)

        if result == _CDT_DATA_NOT_STORED:
            # Call successful, but data is not available
            return
        elif result == _CDT_ERROR_INVALID_INPUTS:
            raise ValueError("Error reading data: Invalid call arguments")
        elif result != _CDT_OK:
            # Something else failed
            raise Exception("Error reading data.")

        return call_outputs

    def _process_array(
            self,
            call_outputs,
            data_key: str,
            len_key: str,
            own_data: bool = True):

        array_length = call_outputs[len_key].value
        if array_length == 0:
            return

        data = numpy.ctypeslib.as_array(call_outputs[data_key], shape=(array_length, ))
        if own_data:
            return data.copy()
        return data

    def _process_data(
            self,
            call_outputs,
            own_data: bool = True):

        shape = []
        dims = []

        # Ordering of multi-dimensional arrays, all possible dimensions:
        # bulk: 'nTime', ('nAxialCells',) ('nRadialCells' / 'nPorts',) 'nComp'
        # particle_liquid: 'nTime', ('nParTypes',) ('nAxialCells',) ('nRadialCells' / 'nPorts',) ('nParShells',) 'nComp'
        # particle_solid: 'nTime', ('nParTypes',) ('nAxialCells',) ('nRadialCells' / 'nPorts',) ('nParShells',) 'nComp', 'nBound'
        # flux: 'nTime', ('nParTypes',) ('nAxialCells',) ('nRadialCells' / 'nPorts',) 'nComp'
        dimensions = [
            'nTime',
            'nParTypes',
            'nAxialCells',
            'nPort',
            'nRadialCells',
            'nParShells',
            'nComp',
            'nBound',
        ]
        for dim in dimensions:
            if dim in call_outputs and call_outputs[dim].value:
                shape.append(call_outputs[dim].value)
                dims.append(dim)

        if len(shape) == 0:
            return

        if 'data' in call_outputs:
            if 'nParShells' in dims:
                nParShells = call_outputs['nParShells'].value
                if nParShells == 1:
                    shape.pop(dims.index('nParShells'))

            data = numpy.ctypeslib.as_array(call_outputs['data'], shape=shape)
            if own_data:
                data = data.copy()

        if 'time' in call_outputs:
            n_time = call_outputs['nTime'].value
            time = numpy.ctypeslib.as_array(call_outputs['time'], shape=(n_time, ))
            if own_data:
                time = time.copy()

        return time, data, dims

    def _load_and_process(self, *args, own_data=True, **kwargs):
        call_outputs = self._load_data(*args, **kwargs)

        if call_outputs is None:
            return

        processed_results = self._process_data(call_outputs, own_data)
        return processed_results

    def _load_and_process_array(self, data_key: str, len_key: str, *args, own_data=True, **kwargs):
        call_outputs = self._load_data(*args, **kwargs)

        if call_outputs is None:
            return None

        return self._process_array(call_outputs, data_key, len_key, own_data)

    def npartypes(self, unitOpId: int):
        call_outputs = self._load_data(
            'getNumParTypes',
            unitOpId=unitOpId,
        )

        return int(call_outputs['nParTypes'].value)

    def nsensitivities(self):
        call_outputs = self._load_data(
            'getNumSensitivities',
        )

        return int(call_outputs['nSens'].value)

    def solution_inlet(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionInlet',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def solution_outlet(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionOutlet',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def solution_bulk(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionBulk',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def solution_particle(self, unitOpId: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSolutionParticle',
            unitOpId=unitOpId,
            parType=parType,
            own_data=own_data,
        )

    def solution_solid(self, unitOpId: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSolutionSolid',
            unitOpId=unitOpId,
            parType=parType,
            own_data=own_data,
        )

    def solution_flux(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionFlux',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def solution_volume(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionVolume',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def soldot_inlet(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeInlet',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def soldot_outlet(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeOutlet',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def soldot_bulk(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeBulk',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def soldot_particle(self, unitOpId: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeParticle',
            unitOpId=unitOpId,
            parType=parType,
            own_data=own_data,
        )

    def soldot_solid(self, unitOpId: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeSolid',
            unitOpId=unitOpId,
            parType=parType,
            own_data=own_data,
        )

    def soldot_flux(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeFlux',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def soldot_volume(self, unitOpId: int, own_data=True):
        return self._load_and_process(
            'getSolutionDerivativeVolume',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def sens_inlet(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityInlet',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sens_outlet(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityOutlet',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sens_bulk(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityBulk',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sens_particle(self, unitOpId: int, sensIdx: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSensitivityParticle',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            parType=parType,
            own_data=own_data,
        )

    def sens_solid(self, unitOpId: int, sensIdx: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSensitivitySolid',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            parType=parType,
            own_data=own_data,
        )

    def sens_flux(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityFlux',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sens_volume(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityVolume',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sensdot_inlet(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeInlet',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sensdot_outlet(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeOutlet',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sensdot_bulk(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeBulk',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sensdot_particle(self, unitOpId: int, sensIdx: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeParticle',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            parType=parType,
            own_data=own_data,
        )

    def sensdot_solid(self, unitOpId: int, sensIdx: int, parType: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeSolid',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            parType=parType,
            own_data=own_data,
        )

    def sensdot_flux(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeFlux',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def sensdot_volume(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getSensitivityDerivativeVolume',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def last_state_y(self, own_data=True):
        return self._load_and_process_array(
            'state',
            'nStates',
            'getLastState',
            own_data=own_data,
        )

    def last_state_ydot(self, own_data=True):
        return self._load_and_process_array(
            'state',
            'nStates',
            'getLastStateTimeDerivative',
            own_data=own_data,
        )

    def last_state_y_unit(self, unitOpId: int, own_data=True):
        return self._load_and_process_array(
            'state',
            'nStates',
            'getLastUnitState',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def last_state_ydot_unit(self, unitOpId: int, own_data=True):
        return self._load_and_process_array(
            'state',
            'nStates',
            'getLastUnitStateTimeDerivative',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def last_state_sens(self, sensIdx: int, own_data=True):
        return self._load_and_process_array(
            'state',
            'nStates',
            'getLastSensitivityState',
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def last_state_sensdot(self, sensIdx: int, own_data=True):
        return self._load_and_process_array(
            'state',
            'nStates',
            'getLastSensitivityStateTimeDerivative',
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def last_state_sens_unit(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getLastSensitivityUnitState',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def last_state_sensdot_unit(self, unitOpId: int, sensIdx: int, own_data=True):
        return self._load_and_process(
            'getLastSensitivityUnitStateTimeDerivative',
            unitOpId=unitOpId,
            sensIdx=sensIdx,
            own_data=own_data,
        )

    def primary_coordinates(self, unitOpId: int, own_data=True):
        return self._load_and_process_array(
            'coords',
            'nCoords',
            'getPrimaryCoordinates',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def secondary_coordinates(self, unitOpId: int, own_data=True):
        return self._load_and_process_array(
            'coords',
            'nCoords',
            'getSecondaryCoordinates',
            unitOpId=unitOpId,
            own_data=own_data,
        )

    def particle_coordinates(self, unitOpId: int, parType: int, own_data=True):
        return self._load_and_process_array(
            'coords',
            'nCoords',
            'getParticleCoordinates',
            unitOpId=unitOpId,
            parType=parType,
            own_data=own_data,
        )

    def solution_times(self, own_data=True):
        return self._load_and_process_array(
            'time',
            'nTime',
            'getSolutionTimes',
            own_data=own_data
        )


class CadetDLL:

    def __init__(self, dll_path):
        self.cadet_path = dll_path
        self._lib = ctypes.cdll.LoadLibrary(dll_path)

        # Query meta information
        cdtGetLibraryVersion = self._lib.cdtGetLibraryVersion
        cdtGetLibraryVersion.restype = ctypes.c_char_p
        self.cadet_version = cdtGetLibraryVersion().decode('utf-8')

        cdtGetLibraryCommitHash = self._lib.cdtGetLibraryCommitHash
        cdtGetLibraryCommitHash.restype = ctypes.c_char_p
        self.cadet_commit_hash = cdtGetLibraryCommitHash().decode('utf-8')

        cdtGetLibraryBranchRefspec = self._lib.cdtGetLibraryBranchRefspec
        cdtGetLibraryBranchRefspec.restype = ctypes.c_char_p
        self.cadet_branch = cdtGetLibraryBranchRefspec().decode('utf-8')

        cdtGetLibraryBuildType = self._lib.cdtGetLibraryBuildType
        cdtGetLibraryBuildType.restype = ctypes.c_char_p
        self.cadet_build_type = cdtGetLibraryBuildType().decode('utf-8')

        # Enable logging
        LOG_HANDLER_CLBK = ctypes.CFUNCTYPE(
            None,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_uint,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_char_p
        )
        set_log_handler = self._lib.cdtSetLogReceiver
        set_log_handler.argtypes = [LOG_HANDLER_CLBK]
        set_log_handler.restype = None
        # Keep reference alive by assigning it to this Python object
        self._log_handler = LOG_HANDLER_CLBK(log_handler)
        set_log_handler(self._log_handler)

        self._set_log_level = self._lib.cdtSetLogLevel
        self._set_log_level.argtypes = [ctypes.c_int]
        self._set_log_level.restype = None
        self._set_log_level(2)

        # Query API
        cdtGetAPIv010000 = self._lib.cdtGetAPIv010000
        cdtGetAPIv010000.argtypes = [ctypes.POINTER(CADETAPIV010000)]
        cdtGetAPIv010000.restype = c_cadet_result

        self._api = CADETAPIV010000()
        cdtGetAPIv010000(ctypes.byref(self._api))

        self._driver = self._api.createDriver()
        self.res = None

    def clear(self):
        if hasattr(self, "res"):
            del self.res
        self._api.deleteDriver(self._driver)
        self._driver = self._api.createDriver()

    def __del__(self):
        log_print('deleteDriver()')
        self._api.deleteDriver(self._driver)

    def run(self, filename=None, simulation=None, timeout=None, check=None):
        pp = cadet_dll_parameterprovider.PARAMETERPROVIDER(simulation)

        self._api.runSimulation(self._driver, ctypes.byref(pp))
        self.res = SimulationResult(self._api, self._driver)

        # TODO: Return if simulation was successful or crashed
        return self.res

    def load_results(self, sim):
        if self.res is None:
            return

        self.load_solution_times(sim)
        self.load_coordinates(sim)
        self.load_solution(sim)
        self.load_sensitivity(sim)
        self.load_state(sim)

    def load_solution_times(self, sim):
        """Load solution_times from simulation results."""
        write_solution_times = sim.root.input['return'].get('write_solution_times', 0)
        if write_solution_times:
            sim.root.output.solution.solution_times = self.res.solution_times()

    def load_coordinates(self, sim):
        """Load coordinates data from simulation results."""
        coordinates = addict.Dict()
        # TODO: Use n_units from API?
        for unit in range(sim.root.input.model.nunits):
            unit_index = self._get_index_string('unit', unit)
            write_coordinates = sim.root.input['return'][unit_index].get('write_coordinates', 0)
            if write_coordinates:
                pc = self.res.primary_coordinates(unit)
                if pc is not None:
                    coordinates[unit_index]['axial_coordinates'] = pc

                sc = self.res.secondary_coordinates(unit)
                if sc is not None:
                    coordinates[unit_index]['radial_coordinates'] = sc

                num_par_types = self.res.npartypes(unit)
                for pt in range(num_par_types):
                    par_coords = self.res.particle_coordinates(unit, pt)
                    if par_coords is not None:
                        par_idx = self._get_index_string('particle_coordinates', pt)
                        coordinates[unit_index][par_idx] = par_coords

        if len(coordinates) > 0:
            sim.root.output.coordinates = coordinates

    def load_solution(self, sim):
        """Load solution data from simulation results."""
        solution = addict.Dict()
        # TODO: Use n_units from API?
        for unit in range(sim.root.input.model.nunits):
            unit_index = self._get_index_string('unit', unit)
            unit_solution = addict.Dict()

            unit_solution.update(self._load_solution_io(sim, unit, 'solution_inlet'))
            unit_solution.update(self._load_solution_io(sim, unit, 'solution_outlet'))
            unit_solution.update(self._load_solution_trivial(sim, unit, 'solution_bulk'))
            unit_solution.update(self._load_solution_particle(sim, unit, 'solution_particle'))
            unit_solution.update(self._load_solution_particle(sim, unit, 'solution_solid'))
            unit_solution.update(self._load_solution_trivial(sim, unit, 'solution_flux'))
            unit_solution.update(self._load_solution_trivial(sim, unit, 'solution_volume'))

            unit_solution.update(self._load_solution_io(sim, unit, 'soldot_inlet'))
            unit_solution.update(self._load_solution_io(sim, unit, 'soldot_outlet'))
            unit_solution.update(self._load_solution_trivial(sim, unit, 'soldot_bulk'))
            unit_solution.update(self._load_solution_particle(sim, unit, 'soldot_particle'))
            unit_solution.update(self._load_solution_particle(sim, unit, 'soldot_solid'))
            unit_solution.update(self._load_solution_trivial(sim, unit, 'soldot_flux'))
            unit_solution.update(self._load_solution_trivial(sim, unit, 'soldot_volume'))

            if len(unit_solution) > 1:
                solution[unit_index].update(unit_solution)

        if len(unit_solution) > 1:
            sim.root.output.solution.update(solution)

        return solution

    def load_sensitivity(self, sim):
        """Load sensitivity data from simulation results."""
        sensitivity = addict.Dict()
        nsens = sim.root.input.sensitivity.get('nsens', 0)

        for sens in range(nsens):
            sens_index = self._get_index_string('param', sens)

            for unit in range(sim.root.input.model.nunits):
                unit_sensitivity = addict.Dict()
                unit_index = self._get_index_string('unit', unit)

                unit_sensitivity.update(
                    self._load_solution_io(sim, unit, 'sens_inlet', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_io(sim, unit, 'sens_outlet', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_trivial(sim, unit, 'sens_bulk', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_particle(sim, unit, 'sens_particle', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_particle(sim, unit, 'sens_solid', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_trivial(sim, unit, 'sens_flux', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_trivial(sim, unit, 'sens_volume', sens)
                )

                unit_sensitivity.update(
                    self._load_solution_io(sim, unit, 'sensdot_inlet', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_io(sim, unit, 'sensdot_outlet', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_trivial(sim, unit, 'sensdot_bulk', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_particle(sim, unit, 'sensdot_particle', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_particle(sim, unit, 'sensdot_solid', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_trivial(sim, unit, 'sensdot_flux', sens)
                )
                unit_sensitivity.update(
                    self._load_solution_trivial(sim, unit, 'sensdot_volume', sens)
                )

                if len(unit_sensitivity) > 0:
                    sensitivity[sens_index][unit_index] = unit_sensitivity

        if len(sensitivity) > 0:
            sim.root.output.sensitivity = sensitivity

    def load_state(self, sim):
        """Load last state from simulation results."""
        # System state
        write_solution_last = sim.root.input['return'].get('write_solution_last', 0)
        if write_solution_last:
            sim.root.output['last_state_y'] = self.res.last_state_y()
            sim.root.output['last_state_ydot'] = self.res.last_state_ydot()

        # System sensitivities
        write_sens_last = sim.root.input['return'].get('write_sens_last', 0)
        if write_sens_last:
            for idx in range(self.res.nsensitivities()):
                idx_str_y = self._get_index_string('last_state_sensy', idx)
                sim.root.output[idx_str_y] = self.res.last_state_sens(idx)
                idx_str_ydot = self._get_index_string('last_state_sensydot', idx)
                sim.root.output[idx_str_ydot] = self.res.last_state_sensdot(idx)


        # TODO: Use n_units from API?
        solution = sim.root.output.solution
        for unit in range(sim.root.input.model.nunits):
            unit_index = self._get_index_string('unit', unit)
            write_solution_last = sim.root.input['return'][unit_index].get('write_solution_last_unit', 0)
            if write_solution_last:
                solution_last_unit = self.res.last_state_y_unit(unit)
                solution[unit_index]['last_state_y'] = solution_last_unit
                soldot_last_unit = self.res.last_state_ydot_unit(unit)
                solution[unit_index]['last_state_ydot'] = soldot_last_unit

    def _checks_if_write_is_true(func):
        """Decorator to check if unit operation solution should be written out."""
        def wrapper(self, sim, unitOpId, solution_str, *args, **kwargs):
            unit_index = self._get_index_string('unit', unitOpId)

            write = sim.root.input['return'][unit_index].get(f'write_{solution_str}', 0)

            if not write:
                return {}

            solution = func(self, sim, unitOpId, solution_str, *args, **kwargs)

            if solution is None:
                return {}

            return solution

        return wrapper

    def _loads_data(func):
        """Decorator to load data from simulation results before processing further."""
        def wrapper(self, sim, unitOpId, solution_str, sensIdx=None, *args, **kwargs):
            solution_fun = getattr(self.res, solution_str)
            if sensIdx is None:
                data = solution_fun(unitOpId)
            else:
                data = solution_fun(unitOpId, sensIdx)

            if data is None:
                return

            solution = func(self, sim, data, unitOpId, solution_str, *args, **kwargs)

            return solution

        return wrapper

    @_checks_if_write_is_true
    @_loads_data
    def _load_solution_trivial(self, sim, data, unitOpId, solution_str, sensIdx=None):
        solution = addict.Dict()
        _, out, _ = data
        solution[solution_str] = out

        return solution

    @_checks_if_write_is_true
    @_loads_data
    def _load_solution_io(self, sim, data, unitOpId, solution_str, sensIdx=None):
        solution = addict.Dict()
        _, out, dims = data

        split_components_data = sim.root.input['return'].get('split_components_data', 1)
        split_ports_data = sim.root.input['return'].get('split_ports_data', 1)
        single_as_multi_port = sim.root.input['return'].get('single_as_multi_port', 0)

        nComp_idx = dims.index('nComp')
        nComp = out.shape[nComp_idx]
        try:
            nPort_idx = dims.index('nPort')
            nPort = out.shape[nPort_idx]
        except ValueError:
            nPort_idx = None
            nPort = 1

        if split_components_data:
            if split_ports_data:
                if nPort == 1:
                    if single_as_multi_port:
                        for comp in range(nComp):
                            comp_out = numpy.squeeze(out[..., comp])
                            solution[f'{solution_str}_port_000_comp_{comp:03d}'] = comp_out
                    else:
                        for comp in range(nComp):
                            comp_out = numpy.squeeze(out[..., comp])
                            solution[f'{solution_str}_comp_{comp:03d}'] = comp_out
                else:
                    for port in range(nPort):
                        for comp in range(nComp):
                            comp_out = numpy.squeeze(out[..., port, comp])
                            solution[f'{solution_str}_port_{port:03d}_comp_{comp:03d}'] = comp_out
            else:
                for comp in range(nComp):
                    comp_out = numpy.squeeze(out[..., comp])
                    solution[f'{solution_str}_comp_{comp:03d}'] = comp_out
        else:
            if split_ports_data:
                if nPort == 1:
                    if single_as_multi_port:
                        solution[f'{solution_str}_port_000'] = out
                    else:
                        solution[solution_str] = numpy.squeeze(out[..., 0, :])
                else:
                    for port in range(nPort):
                        port_out = numpy.squeeze(out[..., port, :])
                        solution[f'{solution_str}_port_{port:03d}'] = port_out
            else:
                if nPort == 1 and nPort_idx is not None:
                    solution[solution_str] = numpy.squeeze(out[..., 0, :])
                else:
                    solution[solution_str] = out

        return solution

    @_checks_if_write_is_true
    def _load_solution_particle(self, sim, unitOpId, solution_str, sensIdx=None):
        solution = addict.Dict()
        solution_fun = getattr(self.res, solution_str)

        npartype = self.res.npartypes(unitOpId)

        for partype in range(npartype):
            if sensIdx is None:
                data = solution_fun(unitOpId, partype)
            else:
                data = solution_fun(unitOpId, sensIdx, partype)

            if data is None:
                continue

            _, out, dims = data

            if npartype == 1:
                solution[solution_str] = out
            else:
                par_index = self._get_index_string('partype', partype)
                solution[f'{solution_str}_{par_index}'] = out

        if len(solution) == 0:
            return

        return solution

    @staticmethod
    def _get_index_string(prefix, index):
        """Helper method to get string indices (e.g. (unit, 0) -> 'unit_000')."""
        return f'{prefix}_{index:03d}'
