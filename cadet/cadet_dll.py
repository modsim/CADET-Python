import ctypes

import addict
import numpy

import cadet.cadet_dll_parameterprovider as cadet_dll_parameterprovider


def log_handler(file, func, line, level, level_name, message):
    log_print('{} ({}:{:d}) {}'.format(
        level_name.decode('utf-8'),
        func.decode('utf-8'),
        line,
        message.decode('utf-8'))
    )


c_cadet_result = ctypes.c_int

array_double = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

point_int = ctypes.POINTER(ctypes.c_int)


def null(*args):
    pass


if 0:
    log_print = print
else:
    log_print = null


class CADETAPIV010000_DATA():
    _data_ = {}
    _data_['createDriver'] = ('drv',)
    _data_['deleteDriver'] = (None, 'drv')
    _data_['runSimulation'] = ('return', 'drv', 'parameterProvider')
    _data_['getNParTypes'] = ('return', 'drv', 'unitOpId', 'nParTypes')
    _data_['getSolutionInlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    _data_['getSolutionOutlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    _data_['getSolutionBulk'] = (
        'return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSolutionParticle'] = (
        'return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime',
        'nParShells', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSolutionSolid'] = (
        'return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime',
        'nParShells', 'nAxialCells', 'nRadialCells', 'nBound'
    )
    _data_['getSolutionFlux'] = (
        'return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp')
    _data_['getSolutionVolume'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime')
    _data_['getSolutionDerivativeInlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    _data_['getSolutionDerivativeOutlet'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nPort', 'nComp')
    _data_['getSolutionDerivativeBulk'] = (
        'return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSolutionDerivativeParticle'] = (
        'return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime',
        'nParShells', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSolutionDerivativeSolid'] = (
        'return', 'drv', 'unitOpId', 'parType', 'time', 'data', 'nTime',
        'nParShells', 'nAxialCells', 'nRadialCells', 'nBound'
    )
    _data_['getSolutionDerivativeFlux'] = (
        'return', 'drv', 'unitOpId', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSolutionDerivativeVolume'] = ('return', 'drv', 'unitOpId', 'time', 'data', 'nTime')
    _data_['getSensitivityInlet'] = ('return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nPort', 'nComp')
    _data_['getSensitivityOutlet'] = ('return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nPort', 'nComp')
    _data_['getSensitivityBulk'] = (
        'return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSensitivityParticle'] = (
        'return', 'drv', 'unitOpId', 'idx', 'parType', 'time', 'data', 'nTime',
        'nParShells', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSensitivitySolid'] = (
        'return', 'drv', 'unitOpId', 'idx', 'parType', 'time', 'data',
        'nTime', 'nParShells', 'nAxialCells', 'nRadialCells', 'nBound'
    )
    _data_['getSensitivityFlux'] = (
        'return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSensitivityVolume'] = ('return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime')
    _data_['getSensitivityDerivativeInlet'] = (
        'return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nPort', 'nComp'
    )
    _data_['getSensitivityDerivativeOutlet'] = (
        'return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nPort', 'nComp'
    )
    _data_['getSensitivityDerivativeBulk'] = (
        'return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSensitivityDerivativeParticle'] = (
        'return', 'drv', 'unitOpId', 'idx', 'parType', 'time', 'data',
        'nTime', 'nParShells', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSensitivityDerivativeSolid'] = (
        'return', 'drv', 'unitOpId', 'idx', 'parType', 'time',
        'data', 'nTime', 'nParShells', 'nAxialCells', 'nRadialCells', 'nBound'
    )
    _data_['getSensitivityDerivativeFlux'] = (
        'return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime', 'nAxialCells', 'nRadialCells', 'nComp'
    )
    _data_['getSensitivityDerivativeVolume'] = ('return', 'drv', 'unitOpId', 'idx', 'time', 'data', 'nTime')

    lookup_prototype = {
        'return': c_cadet_result,
        'drv': ctypes.c_void_p,
        'unitOpId': ctypes.c_int,
        'idx': ctypes.c_int,
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
        None: None,
        'parameterProvider': ctypes.POINTER(cadet_dll_parameterprovider.PARAMETERPROVIDER)
    }

    lookup_call = {
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
    }


def setup_api():
    _fields_ = []

    for key, value in CADETAPIV010000_DATA._data_.items():
        args = tuple(CADETAPIV010000_DATA.lookup_prototype[key] for key in value)
        _fields_.append((key, ctypes.CFUNCTYPE(*args)))

    return _fields_


class CADETAPIV010000(ctypes.Structure):
    _fields_ = setup_api()


def null(obj):
    """do nothing"""
    return obj


class SimulationResult:

    def __init__(self, api, driver):
        self._api = api
        self._driver = driver

    def load_data(self, unit, get_solution, get_solution_str, idx=None, parType=None, own_data=True):
        vars = {}
        wrappers = {}
        for key in CADETAPIV010000_DATA._data_[get_solution_str]:
            if key == 'return':
                continue
            elif key == 'drv':
                vars['drv'] = self._driver
                wrappers[key] = null
            elif key == 'unitOpId':
                vars['unitOpId'] = unit
                wrappers[key] = null
            elif key == 'idx':
                vars['idx'] = idx
                wrappers[key] = null
            elif key == 'parType':
                vars['parType'] = parType
                wrappers[key] = null
            else:
                vars[key] = CADETAPIV010000_DATA.lookup_call[key]()
                wrappers[key] = ctypes.byref

        result = get_solution(*tuple(wrappers[var_key](var_value) for var_key, var_value in vars.items()))

        shape = []
        dims = []
        dimensions = ['nTime', 'nPort', 'nParShells', 'nAxialCells', 'nRadialCells', 'nComp', 'nBound']
        for dim in dimensions:
            if dim in vars and vars[dim].value:
                shape.append(vars[dim].value)
                dims.append(dim)

        data = numpy.ctypeslib.as_array(vars['data'], shape=shape)
        time = numpy.ctypeslib.as_array(vars['time'], shape=(vars['nTime'].value,))

        if own_data:
            return time.copy(), data.copy(), dims
        else:
            return time, data, dims

    def inlet(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionInlet, 'getSolutionInlet', own_data=own_data)

    def outlet(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionOutlet, 'getSolutionOutlet', own_data=own_data)

    def bulk(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionBulk, 'getSolutionBulk', own_data=own_data)

    def particle(self, unit, parType, own_data=True):
        return self.load_data(unit, self._api.getSolutionBulk, 'getSolutionBulk', own_data=own_data)

    def solid(self, unit, parType, own_data=True):
        return self.load_data(unit, self._api.getSolutionSolid, 'getSolutionSolid', own_data=own_data)

    def flux(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionFlux, 'getSolutionFlux', own_data=own_data)

    def volume(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionVolume, 'getSolutionVolume', own_data=own_data)

    def derivativeInlet(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeInlet, 'getSolutionDerivativeInlet',
                              own_data=own_data)

    def derivativeOutlet(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeOutlet, 'getSolutionDerivativeOutlet',
                              own_data=own_data)

    def derivativeBulk(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeBulk, 'getSolutionDerivativeBulk', own_data=own_data)

    def derivativeParticle(self, unit, parType, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeParticle, 'getSolutionDerivativeParticle',
                              own_data=own_data)

    def derivativeSolid(self, unit, parType, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeSolid, 'getSolutionDerivativeSolid',
                              own_data=own_data)

    def derivativeFlux(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeFlux, 'getSolutionDerivativeFlux', own_data=own_data)

    def derivativeVolume(self, unit, own_data=True):
        return self.load_data(unit, self._api.getSolutionDerivativeVolume, 'getSolutionDerivativeVolume',
                              own_data=own_data)

    def sensitivityInlet(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityInlet, 'getSensitivityInlet', idx=idx, own_data=own_data)

    def sensitivityOutlet(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityOutlet, 'getSensitivityOutlet', idx=idx, own_data=own_data)

    def sensitivityBulk(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityBulk, 'getSensitivityBulk', idx=idx, own_data=own_data)

    def sensitivityParticle(self, unit, idx, parType, own_data=True):
        return self.load_data(unit, self._api.getSensitivityParticle, 'getSensitivityParticle', idx=idx,
                              parType=parType, own_data=own_data)

    def sensitivitySolid(self, unit, idx, parType, own_data=True):
        return self.load_data(unit, self._api.getSensitivitySolid, 'getSensitivitySolid', idx=idx, parType=parType,
                              own_data=own_data)

    def sensitivityFlux(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityFlux, 'getSensitivityFlux', idx=idx, own_data=own_data)

    def sensitivityVolume(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityVolume, 'getSensitivityVolume', idx=idx, own_data=own_data)

    def sensitivityDerivativeInlet(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeInlet, 'getSensitivityDerivativeInlet', idx=idx,
                              own_data=own_data)

    def sensitivityDerivativeOutlet(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeOutlet, 'getSensitivityDerivativeOutlet', idx=idx,
                              own_data=own_data)

    def sensitivityDerivativeBulk(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeBulk, 'getSensitivityDerivativeBulk', idx=idx,
                              own_data=own_data)

    def sensitivityDerivativeParticle(self, unit, idx, parType, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeParticle, 'getSensitivityDerivativeParticle',
                              idx=idx, parType=parType, own_data=own_data)

    def sensitivityDerivativeSolid(self, unit, idx, parType, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeSolid, 'getSensitivityDerivativeSolid', idx=idx,
                              parType=parType, own_data=own_data)

    def sensitivityDerivativeFlux(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeFlux, 'getSensitivityDerivativeFlux', idx=idx,
                              own_data=own_data)

    def sensitivityDerivativeVolume(self, unit, idx, own_data=True):
        return self.load_data(unit, self._api.getSensitivityDerivativeVolume, 'getSensitivityDerivativeVolume', idx=idx,
                              own_data=own_data)


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
        return self.res

    def load_solution(self, sim, solution_fun, solution_str):
        # - [ ] Split Ports (incl `SINGLE_AS_MULTI_PORT`)
        # - [ ] Split Partype (Particle + Solid)
        # - [ ] Coordinates?
        # - [ ] Sensitivities / IDs
        # - [ ] LAST_STATE_Y / LAST_STATE_YDOT
        # - [ ] LAST_STATE_SENSY_XXX / LAST_STATE_SENSYDOT_XXX
        solution = addict.Dict()
        if self.res is not None:
            for key, value in sim.root.input['return'].items():
                if key.startswith('unit'):
                    if value[f'write_{solution_str}']:
                        unit = int(key[-3:])
                        t, out, dims = solution_fun(unit)

                        if not len(solution.solution_times):
                            solution.solution_times = t

                        solution[key][solution_str] = out
        return solution

    def load_solution_io(self, sim, solution_fun, solution_str):
        solution = addict.Dict()
        if self.res is not None:
            for key, value in sim.root.input['return'].items():
                if key.startswith('unit'):
                    if value[f'write_{solution_str}']:
                        unit = int(key[-3:])
                        t, out, dims = solution_fun(unit)

                        if not len(solution.solution_times):
                            solution.solution_times = t

                        split_components_data = value.get('split_components_data', 1)
                        split_ports_data = value.get('split_ports_data', 1)
                        single_as_multi_port = value.get('single_as_multi_port', 0)

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
                                            solution[key][f'{solution_str}_port_000_comp_{comp:03d}'] = comp_out
                                    else:
                                        for comp in range(out.shape[nComp]):
                                            comp_out = numpy.squeeze(out[..., comp])
                                            solution[key][f'{solution_str}_comp_{comp:03d}'] = comp_out
                                else:
                                    for port in range(out.shape[nPorts]):
                                        for comp in range(out.shape[nComp]):
                                            comp_out = numpy.squeeze(out[..., port, comp])
                                            solution[key][f'{solution_str}_port_{port:03d}_comp_{comp:03d}'] = comp_out
                            else:
                                for comp in range(out.shape[nComp]):
                                    comp_out = numpy.squeeze(out[..., comp])
                                    solution[key][f'{solution_str}_comp_{comp:03d}'] = comp_out
                        else:
                            if split_ports_data:
                                if nPorts is None:
                                    if single_as_multi_port:
                                        solution[key][f'{solution_str}_port_000'] = out
                                    else:
                                        solution[key][solution_str] = out
                                else:
                                    for port in range(out.shape[nPorts]):
                                        port_out = numpy.squeeze(out[..., port, :])
                                        solution[key][f'{solution_str}_port_{port:03d}'] = port_out
                            else:
                                solution[key][solution_str] = out
        return solution

    def load_inlet(self, sim):
        return self.load_solution_io(sim, self.res.inlet, 'solution_inlet')

    def load_outlet(self, sim):
        return self.load_solution_io(sim, self.res.outlet, 'solution_outlet')

    def load_bulk(self, sim):
        return self.load_solution(sim, self.res.bulk, 'solution_bulk')

    def load_particle(self, sim):
        return self.load_solution(sim, self.res.particle, 'solution_particle')

    def load_solid(self, sim):
        return self.load_solution(sim, self.res.solid, 'solution_solid')

    def load_flux(self, sim):
        return self.load_solution(sim, self.res.flux, 'solution_flux')

    def load_flux(self, sim):
        return self.load_solution(sim, self.res.flux, 'solution_flux')

    def load_volume(self, sim):
        return self.load_solution(sim, self.res.volume, 'solution_volume')

    def load_derivative_inlet(self, sim):
        return self.load_solution_io(sim, self.res.derivativeInlet, 'soldot_inlet')

    def load_derivative_outlet(self, sim):
        return self.load_solution_io(sim, self.res.derivativeOutlet, 'soldot_outlet')

    def load_derivative_bulk(self, sim):
        return self.load_solution(sim, self.res.derivativeBulk, 'soldot_bulk')

    def load_derivative_particle(self, sim):
        return self.load_solution(sim, self.res.derivativeParticle, 'soldot_particle')

    def load_derivative_solid(self, sim):
        return self.load_solution(sim, self.res.derivativeSolid, 'soldot_solid')

    def load_derivative_flux(self, sim):
        return self.load_solution(sim, self.res.derivativeFlux, 'soldot_flux')

    def load_derivative_volume(self, sim):
        return self.load_solution(sim, self.res.derivativeVolume, 'soldot_volume')

    def load_sensitivity_inlet(self, sim):
        return self.load_solution_io(sim, self.res.sensitivityInlet, 'sens_inlet')

    def load_sensitivity_outlet(self, sim):
        return self.load_solution_io(sim, self.res.sensitivityOutlet, 'sens_outlet')

    def load_sensitivity_bulk(self, sim):
        return self.load_solution(sim, self.res.sensitivityBulk, 'sens_bulk')

    def load_sensitivity_particle(self, sim):
        return self.load_solution(sim, self.res.sensitivityParticle, 'sens_particle')

    def load_sensitivity_solid(self, sim):
        return self.load_solution(sim, self.res.sensitivitySolid, 'sens_solid')

    def load_sensitivity_flux(self, sim):
        return self.load_solution(sim, self.res.sensitivityFlux, 'sens_flux')

    def load_sensitivity_volume(self, sim):
        return self.load_solution(sim, self.res.sensitivityVolume, 'sens_volume')

    def load_sensitivity_derivative_inlet(self, sim):
        return self.load_solution_io(sim, self.res.sensitivityDerivativeInlet, 'sensdot_inlet')

    def load_sensitivity_derivative_outlet(self, sim):
        return self.load_solution_io(sim, self.res.sensitivityDerivativeOutlet, 'sensdot_outlet')

    def load_sensitivity_derivative_bulk(self, sim):
        return self.load_solution(sim, self.res.sensitivityDerivativeBulk, 'sensdot_bulk')

    def load_sensitivity_derivative_particle(self, sim):
        return self.load_solution(sim, self.res.sensitivityDerivativeParticle, 'sensdot_particle')

    def load_sensitivity_derivative_solid(self, sim):
        return self.load_solution(sim, self.res.sensitivityDerivativeSolid, 'sensdot_solid')

    def load_sensitivity_derivative_flux(self, sim):
        return self.load_solution(sim, self.res.sensitivityDerivativeFlux, 'sensdot_flux')

    def load_sensitivity_derivative_volume(self, sim):
        return self.load_solution(sim, self.res.sensitivityDerivativeVolume, 'sensdot_volume')

    def load_results(self, sim):
        sim.root.output.solution.update(self.load_inlet(sim))
        sim.root.output.solution.update(self.load_outlet(sim))
        sim.root.output.solution.update(self.load_bulk(sim))
        sim.root.output.solution.update(self.load_particle(sim))
        sim.root.output.solution.update(self.load_solid(sim))
        sim.root.output.solution.update(self.load_flux(sim))
        sim.root.output.solution.update(self.load_volume(sim))
        sim.root.output.solution.update(self.load_derivative_inlet(sim))
        sim.root.output.solution.update(self.load_derivative_outlet(sim))
        sim.root.output.solution.update(self.load_derivative_bulk(sim))
        sim.root.output.solution.update(self.load_derivative_particle(sim))
        sim.root.output.solution.update(self.load_derivative_solid(sim))
        sim.root.output.solution.update(self.load_derivative_flux(sim))
        sim.root.output.solution.update(self.load_derivative_volume(sim))
        # sim.root.output.solution.update(self.load_sensitivity_inlet(sim))
        # sim.root.output.solution.update(self.load_sensitivity_outlet(sim))
        # sim.root.output.solution.update(self.load_sensitivity_bulk(sim))
        # sim.root.output.solution.update(self.load_sensitivity_particle(sim))
        # sim.root.output.solution.update(self.load_sensitivity_solid(sim))
        # sim.root.output.solution.update(self.load_sensitivity_flux(sim))
        # sim.root.output.solution.update(self.load_sensitivity_volume(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_inlet(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_outlet(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_bulk(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_particle(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_solid(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_flux(sim))
        # sim.root.output.solution.update(self.load_sensitivity_derivative_volume(sim))
