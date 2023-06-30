import ctypes
import numpy
import addict
import cadet.cadet_dll_parameterprovider as cadet_dll_parameterprovider


def log_handler(file, func, line, level, level_name, message):
    log_print('{} ({}:{:d}) {}'.format(level_name.decode('utf-8') , func.decode('utf-8') , line, message.decode('utf-8') ))


c_cadet_result = ctypes.c_int

array_double = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))


point_int = ctypes.POINTER(ctypes.c_int)
CadetDriver = ctypes.c_void_p

# Values of cdtResult
_CDT_OK = 0
_CDT_DATA_NOT_STORED = -3


def _no_log_output(*args):
    pass


if 0:
    log_print = print
else:
    log_print = _no_log_output


class CADETAPIV010000_DATA():
    """
    Definition of CADET-CAPI v1.0

    signatures : dict with signatures of exported API functions. (See CADET/include/cadet/cadet.h)
    lookup_prototype : ctypes for common parameters
    lookup_output_argument_type : ctypes for API output parameters (e.g., double* time or double** data)

    """

    # Order is important, has to match the cdtAPIv010000 struct of the C-API
    signatures = {}
    signatures['createDriver'] = ('drv',)
    signatures['deleteDriver'] = (None, 'drv')
    signatures['runSimulation'] = ('return', 'drv', 'parameterProvider')
    signatures['getNParTypes'] = ('return', 'drv', 'unitOpId', 'nParTypes')

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


    lookup_prototype = {
        'return': c_cadet_result,
        'drv': CadetDriver,
        'unitOpId': ctypes.c_int,
        'sensIdx': ctypes.c_int,
        'parType': ctypes.c_int,
        'time': array_double,
        'data': array_double,
        'nTime': point_int,
        'nPort': point_int,
        'nAxialCells': point_int,
        'nRadialCells': point_int,
        'nParTypes': point_int,
        'nParShells': point_int,
        'nComp': point_int,
        'nBound': point_int,
        'state': array_double,
        'nStates': point_int,
        None: None,
        'parameterProvider': ctypes.POINTER(cadet_dll_parameterprovider.PARAMETERPROVIDER)
    }

    lookup_output_argument_type = {
        'time': ctypes.POINTER(ctypes.c_double),
        'nTime': ctypes.c_int,
        'data': ctypes.POINTER(ctypes.c_double),
        'nPort': ctypes.c_int,
        'nAxialCells': ctypes.c_int,
        'nRadialCells': ctypes.c_int,
        'nParTypes': ctypes.c_int,
        'nParShells': ctypes.c_int,
        'nComp': ctypes.c_int,
        'nBound': ctypes.c_int,
        'state': ctypes.POINTER(ctypes.c_double),
        'nStates': ctypes.c_int,
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

    def load_data(
            self,
            get_solution_str: str,
            unitOpId: int | None,
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
            return None
        elif result != _CDT_OK:
            # Something else failed
            raise Exception("Error reading data.")

        return call_outputs

    def process_data(
            self,
            call_outputs,
            own_data: bool = True):

        shape = []
        dims = []

        # Ordering of multi-dimensional arrays, all possible dimensions:
        # Example: Outlet [nTime, nPort, nComp]
        #          Bulk [nTime, nRadialCells, nAxialCells, nComp] if 2D model
        #          Bulk [nTime, nAxialCells, nComp] if 1D model
        dimensions = ['nTime', 'nPort', 'nRadialCells', 'nAxialCells', 'nParShells', 'nComp', 'nBound']
        for dim in dimensions:
            if dim in call_outputs and call_outputs[dim].value:
                shape.append(call_outputs[dim].value)
                dims.append(dim)

        data = numpy.ctypeslib.as_array(call_outputs['data'], shape=shape)
        time = numpy.ctypeslib.as_array(call_outputs['time'], shape=(call_outputs['nTime'].value, ))

        if own_data:
            return time.copy(), data.copy(), dims
        else:
            return time, data, dims

    def load_and_process(self, *args, own_data=True, **kwargs):
        call_outputs = self.load_data(*args, **kwargs)

        if call_outputs is None:
            return None, None, None

        time, data, dims = self.process_data(call_outputs, own_data)

        return time, data, dims

    def load_data_old(
            self,
            get_solution_str: str,
            unitOpId: int | None,
            sensIdx: int = None,
            parType: int = None,
            own_data: bool = True):

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
            return None, None, None
        elif result != _CDT_OK:
            # Something else failed
            raise Exception("Error reading data.")

        shape = []
        dims = []

        # Ordering of multi-dimensional arrays, all possible dimensions:
        # Example: Outlet [nTime, nPort, nComp]
        #          Bulk [nTime, nRadialCells, nAxialCells, nComp] if 2D model
        #          Bulk [nTime, nAxialCells, nComp] if 1D model
        dimensions = ['nTime', 'nPort', 'nRadialCells', 'nAxialCells', 'nParShells', 'nComp', 'nBound']
        for dim in dimensions:
            if dim in call_outputs and call_outputs[dim].value:
                shape.append(call_outputs[dim].value)
                dims.append(dim)

        data = numpy.ctypeslib.as_array(call_outputs['data'], shape=shape)
        time = numpy.ctypeslib.as_array(call_outputs['time'], shape=(call_outputs['nTime'].value, ))

        if own_data:
            return time.copy(), data.copy(), dims
        else:
            return time, data, dims

    def npartypes(self, unitOpId: int, own_data=True):
        call_outputs = self.load_data(
            'getNParTypes',
            unitOpId,
        )

        return int(numpy.ctypeslib.as_array(call_outputs['nParTypes']))

    def solution_inlet(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionInlet',
            unitOpId,
            own_data=own_data
        )

    def solution_outlet(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionOutlet',
            unitOpId,
            own_data=own_data
        )

    def solution_bulk(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionBulk',
            unitOpId,
            own_data=own_data
        )

    def solution_particle(self, unitOpId: int, parType, own_data=True):
        return self.load_and_process(
            'getSolutionParticle',
            unitOpId,
            parType=parType,
            own_data=own_data
        )

    def solution_solid(self, unitOpId: int, parType, own_data=True):
        return self.load_and_process(
            'getSolutionSolid',
            unitOpId,
            parType=parType,
            own_data=own_data
        )

    def solution_flux(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionFlux',
            unitOpId,
            own_data=own_data
        )

    def solution_volume(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionVolume',
            unitOpId,
            own_data=own_data
        )

    def soldot_inlet(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeInlet',
            unitOpId,
            own_data=own_data
        )

    def soldot_outlet(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeOutlet',
            unitOpId,
            own_data=own_data
        )

    def soldot_bulk(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeBulk',
            unitOpId,
            own_data=own_data
        )

    def soldot_particle(self, unitOpId: int, parType: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeParticle',
            unitOpId,
            parType=parType,
            own_data=own_data
        )

    def soldot_solid(self, unitOpId: int, parType: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeSolid',
            unitOpId,
            parType=parType,
            own_data=own_data
        )

    def soldot_flux(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeFlux',
            unitOpId,
            own_data=own_data
        )

    def soldot_volume(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getSolutionDerivativeVolume',
            unitOpId,
            own_data=own_data
        )

    def sens_inlet(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityInlet',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sens_outlet(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityOutlet',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sens_bulk(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityBulk',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sens_particle(self, unitOpId: int, sensIdx, parType: int, own_data=True):
        return self.load_and_process(
            'getSensitivityParticle',
            unitOpId,
            sensIdx=sensIdx,
            parType=parType, own_data=own_data
        )

    def sens_solid(self, unitOpId: int, sensIdx, parType, own_data=True):
        return self.load_and_process(
            'getSensitivitySolid',
            unitOpId,
            sensIdx=sensIdx,
            parType=parType, own_data=own_data
        )

    def sens_flux(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityFlux',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sens_volume(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityVolume',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sensdot_inlet(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeInlet',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sensdot_outlet(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeOutlet',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sensdot_bulk(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeBulk',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sensdot_particle(self, unitOpId: int, sensIdx, parType, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeParticle',
            unitOpId,
            sensIdx=sensIdx,
            parType=parType, own_data=own_data
        )

    def sensdot_solid(self, unitOpId: int, sensIdx, parType, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeSolid',
            unitOpId,
            sensIdx=sensIdx,
            parType=parType, own_data=own_data
        )

    def sensdot_flux(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeFlux',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def sensdot_volume(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getSensitivityDerivativeVolume',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def last_state_y(self, own_data=True):
        return self.load_and_process(
            'getLastState',
            own_data=own_data
        )

    def last_state_ydot(self, sensIdx, own_data=True):
        return self.load_and_process(
            'getLastStateDerivative',
            own_data=own_data
        )

    def last_state_y_unit(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getLastUnitState',
            unitOpId,
            own_data=own_data
        )

    def last_state_ydot_unit(self, unitOpId: int, own_data=True):
        return self.load_and_process(
            'getLastUnitStateTimeDerivative',
            unitOpId,
            own_data=own_data
        )

    def last_state_sens(self, sensIdx, own_data=True):
        return self.load_and_process(
            'getLastSensitivityState',
            sensIdx=sensIdx,
            own_data=own_data
        )

    def last_state_sensdot(self, sensIdx, own_data=True):
        return self.load_and_process(
            'getLastSensitivityStateTimeDerivative',
            sensIdx=sensIdx,
            own_data=own_data
        )

    def last_state_sens_unit(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getLastSensitivityUnitState',
            unitOpId,
            sensIdx=sensIdx,
            own_data=own_data
        )

    def last_state_sensdot_unit(self, unitOpId: int, sensIdx, own_data=True):
        return self.load_and_process(
            'getLastSensitivityUnitStateTimeDerivative',
            unitOpId,
            sensIdx=sensIdx,
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
        # TODO: solution time
        # sim.root.output.solution.solution_time = ???
        self.load_coordinates(sim)
        # TODO: Crashes when simulation includes sensitivities
        self.load_solution(sim)
        self.load_sensitivity(sim)
        self.load_state(sim)

    def load_coordinates(self, sim):
        coordinates = addict.Dict()
        for unit in range(sim.root.input.model.nunits):
            unit_index = self._get_index_string('unit', unit)
            if 'write_coordinates' in sim.root.input['return'][unit_index].keys():
                # TODO: Missing CAPI call
                pass

        sim.root.output.coordinates = coordinates

    def load_solution(self, sim):
        solution = addict.Dict()
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
            sim.root.output.solution = solution

        return solution

    def load_sensitivity(self, sim):
        sensitivity = addict.Dict()
        nsens = sim.root.input.sensitivity.get('nsens', 0)
        for sens in range(nsens):
            sens_index = self._get_index_string('param', sens)
            for unit in range(sim.root.input.model.nunits):
                unit_sensitivity = addict.Dict()

                unit_sensitivity[sens_index].update(
                    self._load_solution_io(sim, unit, 'sens_inlet', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_io(sim, unit, 'sens_outlet', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_trivial(sim, unit, 'sens_bulk', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_particle(sim, unit, 'sens_particle', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_particle(sim, unit, 'sens_solid', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_trivial(sim, unit, 'sens_flux', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_trivial(sim, unit, 'sens_volume', sens)
                )

                unit_sensitivity[sens_index].update(
                    self._load_solution_io(sim, unit, 'sensdot_inlet', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_io(sim, unit, 'sensdot_outlet', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_trivial(sim, unit, 'sensdot_bulk', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_particle(sim, unit, 'sensdot_particle', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_particle(sim, unit, 'sensdot_solid', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_trivial(sim, unit, 'sensdot_flux', sens)
                )
                unit_sensitivity[sens_index].update(
                    self._load_solution_trivial(sim, unit, 'sensdot_volume', sens)
                )

            sensitivity[sens_index].update(unit_sensitivity)

        sim.root.output.sensitivity = sensitivity

    def _checks_if_write_is_true(func):
        def wrapper(self, sim, unitOpId, solution_str, *args, **kwargs):
            unit_index = self._get_index_string('unit', unitOpId)
            solution_recorder = sim.root.input['return'][unit_index].keys()
            if f'write_{solution_str}' not in solution_recorder:
                return {}

            solution = func(self, sim, unitOpId, solution_str, *args, **kwargs)

            if solution is None:
                return {}

            return solution

        return wrapper

    def _loads_data(func):
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
        t, out, dims = data
        solution[solution_str] = out

        return solution

    @_checks_if_write_is_true
    @_loads_data
    def _load_solution_io(self, sim, data, unitOpId, solution_str, sensIdx=None):
        solution = addict.Dict()
        t, out, dims = data

        split_components_data = sim.root.input['return'].get('split_components_data', 1)
        split_ports_data = sim.root.input['return'].get('split_ports_data', 1)
        single_as_multi_port = sim.root.input['return'].get('single_as_multi_port', 0)

        nComp = dims.index('nComp')
        try:
            nPorts = dims.index('nPorts')
        except ValueError:
            nPorts = None

        if split_components_data:
            if split_ports_data:
                if nPorts is None:
                    if single_as_multi_port:
                        for comp in range(out.shape[nComp]):
                            comp_out = numpy.squeeze(out[..., comp])
                            solution[f'{solution_str}_port_000_comp_{comp:03d}'] = comp_out
                    else:
                        for comp in range(out.shape[nComp]):
                            comp_out = numpy.squeeze(out[..., comp])
                            solution[f'{solution_str}_comp_{comp:03d}'] = comp_out
                else:
                    for port in range(out.shape[nPorts]):
                        for comp in range(out.shape[nComp]):
                            comp_out = numpy.squeeze(out[..., port, comp])
                            solution[f'{solution_str}_port_{port:03d}_comp_{comp:03d}'] = comp_out
            else:
                for comp in range(out.shape[nComp]):
                    comp_out = numpy.squeeze(out[..., comp])
                    solution[f'{solution_str}_comp_{comp:03d}'] = comp_out
        else:
            if split_ports_data:
                if nPorts is None:
                    if single_as_multi_port:
                        solution[f'{solution_str}_port_000'] = out
                    else:
                        solution[solution_str] = out
                else:
                    for port in range(out.shape[nPorts]):
                        port_out = numpy.squeeze(out[..., port, :])
                        solution[f'{solution_str}_port_{port:03d}'] = port_out
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

            t, out, dims = data

            if npartype == 1:
                solution[solution_str] = out
            else:
                par_index = self._get_index_string('partype', partype)
                solution[f'{solution_str}_{par_index}'] = out

        if len(solution) == 0:
            return

        return solution

    def _load_particle_type(self, sim, data, unitOpId, solution_str, sensIdx=None):
        pass

    def load_state(self, sim):
        # TODO
        pass

    @staticmethod
    def _get_index_string(prefix, index):
        return f'{prefix}_{index:03d}'
