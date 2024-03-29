import copy
import os
from pathlib import Path
import platform
import subprocess
import sys

from addict import Dict
import pytest

from cadet import Cadet


# %% Utility methods

# TODO: Remove once #5 is merged
cadet_root = Path('/home/jo/code/CADET/install/capi/')

def setup_model(
        cadet_root,
        use_dll=True,
        model='GENERAL_RATE_MODEL',
        n_partypes=1,
        include_sensitivity=False,
        file_name='LWE.h5',
        ):
    """
    Set up and initialize a CADET model template.

    This function prepares a CADET model template by invoking the `createLWE` executable
    with specified parameters. It supports the configuration of the model type, number
    of particle types, inclusion of sensitivity analysis, and the name of the output
    file. Depending on the operating system, it adjusts the executable name accordingly.
    After creating the model, it initializes a Cadet instance with the specified or
    default CADET binary and the created model file.

    Parameters
    ----------
    cadet_root : str or Path
        The root directory where the CADET software is located.
    use_dll : bool, optional
        If True, use the in-memory interface for CADET. Otherwise, use the CLI.
        The default is True.
    model : str, optional
        The model type to set up. The default is 'GENERAL_RATE_MODEL'.
    n_partypes : int, optional
        The number of particle types. The default is 1.
    include_sensitivity : bool, optional
        If True, included parameter sensitivities in template. The default is False.
    file_name : str, optional
        The name of the file to which the CADET model is written.
        The default is 'LWE.h5'.

    Returns
    -------
    Cadet
        An initialized Cadet instance with the model loaded.

    Raises
    ------
    Exception
        If the creation of the test simulation encounters problems,
        detailed in the subprocess's stdout and stderr.
    FileNotFoundError
        If the CADET executable or DLL file cannot be found at the specified paths.

    Notes
    -----
    The function assumes the presence of `createLWE` executable within the `bin`
    directory of the `cadet_root` path. The sensitivity analysis, if included, is
    configured for column porosity.

    See Also
    --------
    Cadet : The class representing a CADET simulation model.

    Examples
    --------
    >>> cadet_model = setup_model(
        '/path/to/cadet',
        use_dll=False,
        model='GENERAL_RATE_MODEL',
        n_partypes=2,
        include_sensitivity=True,
        file_name='my_model.h5'
    )
    This example sets up a GENERAL_RATE_MODEL with 2 particle types, includes
    sensitivity analysis, and writes the model to 'my_model.h5', using the command-line
    interface.
    """
    executable = 'createLWE'
    if platform.system() == 'Windows':
        executable += '.exe'

    create_lwe_path = Path(cadet_root) / 'bin' / executable

    args =[
        create_lwe_path.as_posix(),
        f'--out {file_name}',
        f'--unit {model}',
        f'--parTypes {n_partypes}',
    ]

    if include_sensitivity:
        args.append('--sens COL_POROSITY/-1/-1/-1/-1/-1/-1/0')

    ret = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='./'
    )

    if ret.returncode != 0:
        if ret.stdout:
            print('Output', ret.stdout.decode('utf-8'))
        if ret.stderr:
            print('Errors', ret.stderr.decode('utf-8'))
        raise Exception(
            "Failure: Creation of test simulation ran into problems"
        )

    model = Cadet()
    # TODO: This should be simplified once #14 is merged.
    if use_dll:
        cadet_path = cadet_root / 'lib' / 'libcadet.so'
        if not cadet_path.exists():
            cadet_path = cadet_root / 'lib' / 'libcadet_d.so'
    else:
        cadet_path = cadet_root / 'bin' / 'cadet-cli'

    if not cadet_path.exists():
        raise FileNotFoundError("Could not find CADET at: {cadet_root}")

    model.cadet_path = cadet_path
    model.filename = file_name
    model.load()

    return model


def setup_solution_recorder(
        model,
        split_components=0,
        split_ports=0,
        single_as_multi_port=0,
        ):
    """
    Configure the solution recorder for the simulation.

    This function adjusts the model's settings to specify what simulation data should
    be recorded, including solutions at various points (inlet, outlet, bulk, etc.),
    sensitivities, and their derivatives. It allows for the configuration of how
    components and ports are treated in the output data, potentially splitting them for
    individual analysis or aggregating them for a more holistic view.

    Parameters
    ----------
    model : Cadet
        The model instance to be configured for solution recording.
    split_components : int, optional
        If 1, split component data in the output. The default is 0.
    split_ports : int, optional
        If 1, split port data in the output. The default is 0.
    single_as_multi_port : int, optional
        If 1, treat single ports as multiple ports in the output. The default is 0.

    Examples
    --------
    >>> model = Cadet()
    >>> setup_solution_recorder(model, split_components=1, split_ports=1, single_as_multi_port=1)
    This example demonstrates configuring a Cadet model instance for detailed solution recording, with component and port data split, and single ports treated as multiple ports.

    """

    model.root.input['return'].write_solution_times = 1
    model.root.input['return'].write_solution_last = 1
    model.root.input['return'].write_sens_last = 1

    model.root.input['return'].split_components_data = split_components
    model.root.input['return'].split_ports_data = split_ports
    model.root.input['return'].single_as_multi_port = single_as_multi_port

    model.root.input['return'].unit_000.write_coordinates = 1

    model.root.input['return'].unit_000.write_solution_inlet = 1
    model.root.input['return'].unit_000.write_solution_outlet = 1
    model.root.input['return'].unit_000.write_solution_bulk = 1
    model.root.input['return'].unit_000.write_solution_particle = 1
    model.root.input['return'].unit_000.write_solution_solid = 1
    model.root.input['return'].unit_000.write_solution_flux = 1
    model.root.input['return'].unit_000.write_solution_volume = 1

    model.root.input['return'].unit_000.write_soldot_inlet = 1
    model.root.input['return'].unit_000.write_soldot_outlet = 1
    model.root.input['return'].unit_000.write_soldot_bulk = 1
    model.root.input['return'].unit_000.write_soldot_particle = 1
    model.root.input['return'].unit_000.write_soldot_solid = 1
    model.root.input['return'].unit_000.write_soldot_flux = 1
    model.root.input['return'].unit_000.write_soldot_volume = 1

    model.root.input['return'].unit_000.write_sens_inlet = 1
    model.root.input['return'].unit_000.write_sens_outlet = 1
    model.root.input['return'].unit_000.write_sens_bulk = 1
    model.root.input['return'].unit_000.write_sens_particle = 1
    model.root.input['return'].unit_000.write_sens_solid = 1
    model.root.input['return'].unit_000.write_sens_flux = 1
    model.root.input['return'].unit_000.write_sens_volume = 1

    model.root.input['return'].unit_000.write_sensdot_inlet = 1
    model.root.input['return'].unit_000.write_sensdot_outlet = 1
    model.root.input['return'].unit_000.write_sensdot_bulk = 1
    model.root.input['return'].unit_000.write_sensdot_particle = 1
    model.root.input['return'].unit_000.write_sensdot_solid = 1
    model.root.input['return'].unit_000.write_sensdot_flux = 1
    model.root.input['return'].unit_000.write_sensdot_volume = 1

    model.root.input['return'].unit_000.write_solution_last_unit = 1
    model.root.input['return'].unit_000.write_soldot_last_unit = 1

    # LAST_STATE_Y
    # LAST_STATE_YDOT
    # LAST_STATE_SENSYDOT_???
    # LAST_STATE_SENSY_???

    for unit in range(model.root.input.model['nunits']):
        model.root.input['return']['unit_{0:03d}'.format(unit)] = model.root.input['return'].unit_000

    if model.filename is not None:
        model.save()


def run_simulation_with_options(use_dll, model_options, solution_recorder_options):
    """Run a simulation with specified options for the model and solution recorder.

    Initializes and configures a simulation model with given options, sets up the
    solution recording parameters, and executes the simulation. This function leverages
    `setup_model` to create and initialize the model and `setup_solution_recorder` to
    configure how the simulation results should be recorded based on the specified
    options.

    Parameters
    ----------
    use_dll : bool, optional
        If True, use the in-memory interface for CADET. Otherwise, use the CLI.
        The default is True.
    model_options : dict
        A dictionary of options to pass to `setup_model` for initializing the model.
        Keys should match the parameter names of `setup_model`, excluding `use_dll`.
    solution_recorder_options : dict
        A dictionary of options to pass to `setup_solution_recorder` for configuring the
        solution recorder. Keys should match the parameter names of
        `setup_solution_recorder`.

    Returns
    -------
    Cadet
        An instance of the Cadet class with the model simulated and loaded.

    Examples
    --------
    >>> use_dll = True
    >>> model_options = {
    ...     'model': 'GENERAL_RATE_MODEL',
    ...     'n_partypes': 2,
    ...     'include_sensitivity': True,
    ...     'file_name': 'model_output.h5'
    ... }
    >>> solution_recorder_options = {
    ...     'split_components': 1,
    ...     'split_ports': 1,
    ...     'single_as_multi_port': True
    ... }
    >>> model = run_simulation_with_options(use_dll, model_options, solution_recorder_options)
    This example configures and runs a GENERAL_RATE_MODEL with sensitivity analysis and two particle types, records the solution with specific options, and loads the simulation results for further analysis.
    """
    model = setup_model(cadet_root, use_dll, **model_options)
    setup_solution_recorder(model, **solution_recorder_options)

    model.run_load()

    return model


# %% Model templates
grm_template = {
    'model': 'GENERAL_RATE_MODEL',
    'n_partypes': 1,
    'include_sensitivity': False,
}

grm_template_sens = {
    'model': 'GENERAL_RATE_MODEL',
    'n_partypes': 1,
    'include_sensitivity': True,
}

grm_template_partypes = {
    'model': 'GENERAL_RATE_MODEL',
    'n_partypes': 2,
    'include_sensitivity': False,
}

_2dgrm_template = {
    'model': 'GENERAL_RATE_MODEL_2D',
    'n_partypes': 1,
    'include_sensitivity': False,
}


# %% Solution recorder templates

no_split_options = {
    'split_components': 0,
    'split_ports': 0,
    'single_as_multi_port': 0,
}

split_ports_options = {
    'split_components': 0,
    'split_ports': 1,
    'single_as_multi_port': 0,
}

split_all_options = {
    'split_components': 1,
    'split_ports': 1,
    'single_as_multi_port': 1,
}

# %% Test cases

class Case():
    def __init__(self, name, model_options, solution_recorder_options, expected_results):
        self.name = name
        self.model_options = model_options
        self.solution_recorder_options = solution_recorder_options
        self.expected_results = expected_results

    def __str__(self):
        return self.name

    def __repr__(self):
        return \
            f"Case('{self.name}', {self.model_options}, " \
            f"{self.solution_recorder_options}, {self.expected_results})"

# %% GRM

grm = Case(
    name='grm',
    model_options=grm_template,
    solution_recorder_options=no_split_options,
    expected_results={
        'last_state_y': (412,),
        'last_state_ydot': (412,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
        },
        'solution_unit_000': {
            'last_state_y': (404,),
            'last_state_ydot': (404,),
            'soldot_bulk': (1501, 10, 4),
            'soldot_flux': (1501, 1, 10, 4),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'soldot_particle': (1501, 10, 4, 4),
            'soldot_solid': (1501, 10, 4, 4),
            'solution_bulk': (1501, 10, 4),
            'solution_flux': (1501, 1, 10, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
            'solution_particle': (1501, 10, 4, 4),
            'solution_solid': (1501, 10, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
        },
    },
)

# %% GRM Split

grm_split = Case(
    name='grm_split',
    model_options=grm_template,
    solution_recorder_options=split_all_options,
    expected_results={
        'last_state_y': (412,),
        'last_state_ydot': (412,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
        },
        'solution_unit_000': {
            'last_state_y': (404,),
            'last_state_ydot': (404,),
            'soldot_bulk': (1501, 10, 4),
            'soldot_flux': (1501, 1, 10, 4),
            'soldot_inlet_port_000_comp_000': (1501,),
            'soldot_inlet_port_000_comp_001': (1501,),
            'soldot_inlet_port_000_comp_002': (1501,),
            'soldot_inlet_port_000_comp_003': (1501,),
            'soldot_outlet_port_000_comp_000': (1501,),
            'soldot_outlet_port_000_comp_001': (1501,),
            'soldot_outlet_port_000_comp_002': (1501,),
            'soldot_outlet_port_000_comp_003': (1501,),
            'soldot_particle': (1501, 10, 4, 4),
            'soldot_solid': (1501, 10, 4, 4),
            'solution_bulk': (1501, 10, 4),
            'solution_flux': (1501, 1, 10, 4),
            'solution_inlet_port_000_comp_000': (1501,),
            'solution_inlet_port_000_comp_001': (1501,),
            'solution_inlet_port_000_comp_002': (1501,),
            'solution_inlet_port_000_comp_003': (1501,),
            'solution_outlet_port_000_comp_000': (1501,),
            'solution_outlet_port_000_comp_001': (1501,),
            'solution_outlet_port_000_comp_002': (1501,),
            'solution_outlet_port_000_comp_003': (1501,),
            'solution_particle': (1501, 10, 4, 4),
            'solution_solid': (1501, 10, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet_port_000_comp_000': (1501,),
            'soldot_inlet_port_000_comp_001': (1501,),
            'soldot_inlet_port_000_comp_002': (1501,),
            'soldot_inlet_port_000_comp_003': (1501,),
            'soldot_outlet_port_000_comp_000': (1501,),
            'soldot_outlet_port_000_comp_001': (1501,),
            'soldot_outlet_port_000_comp_002': (1501,),
            'soldot_outlet_port_000_comp_003': (1501,),
            'solution_inlet_port_000_comp_000': (1501,),
            'solution_inlet_port_000_comp_001': (1501,),
            'solution_inlet_port_000_comp_002': (1501,),
            'solution_inlet_port_000_comp_003': (1501,),
            'solution_outlet_port_000_comp_000': (1501,),
            'solution_outlet_port_000_comp_001': (1501,),
            'solution_outlet_port_000_comp_002': (1501,),
            'solution_outlet_port_000_comp_003': (1501,),
        },
    },
)

# %% GRM Sens

grm_sens = Case(
    name='grm_sens',
    model_options=grm_template_sens,
    solution_recorder_options=no_split_options,
    expected_results={
        'last_state_y': (412,),
        'last_state_ydot': (412,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
        },
        'solution_unit_000': {
            'last_state_y': (404,),
            'last_state_ydot': (404,),
            'soldot_bulk': (1501, 10, 4),
            'soldot_flux': (1501, 1, 10, 4),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'soldot_particle': (1501, 10, 4, 4),
            'soldot_solid': (1501, 10, 4, 4),
            'solution_bulk': (1501, 10, 4),
            'solution_flux': (1501, 1, 10, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
            'solution_particle': (1501, 10, 4, 4),
            'solution_solid': (1501, 10, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
        },
        'sens_param_000_unit_000': {
            'sensdot_bulk': (1501, 10, 4),
            'sensdot_flux': (1501, 1, 10, 4),
            'sensdot_inlet': (1501, 4),
            'sensdot_outlet': (1501, 4),
            'sensdot_particle': (1501, 10, 4, 4),
            'sensdot_solid': (1501, 10, 4, 4),
            'sens_bulk': (1501, 10, 4),
            'sens_flux': (1501, 1, 10, 4),
            'sens_inlet': (1501, 4),
            'sens_outlet': (1501, 4),
            'sens_particle': (1501, 10, 4, 4),
            'sens_solid': (1501, 10, 4, 4),
        },
        'sens_param_000_unit_001': {
            'sensdot_inlet': (1501, 4),
            'sensdot_outlet': (1501, 4),
            'sens_inlet': (1501, 4),
            'sens_outlet': (1501, 4),
        },
    },
)

# %% GRM ParTypes

grm_par_types = Case(
    name='grm_par_types',
    model_options=grm_template_partypes,
    solution_recorder_options=no_split_options,
    expected_results={
        'last_state_y': (772,),
        'last_state_ydot': (772,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
            'particle_coordinates_001': (4,),
        },
        'solution_unit_000': {
            'last_state_y': (764,),
            'last_state_ydot': (764,),
            'soldot_bulk': (1501, 10, 4),
            'soldot_flux': (1501, 2, 10, 4),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'soldot_particle_partype_000': (1501, 10, 4, 4),
            'soldot_particle_partype_001': (1501, 10, 4, 4),
            'soldot_solid_partype_000': (1501, 10, 4, 4),
            'soldot_solid_partype_001': (1501, 10, 4, 4),
            'solution_bulk': (1501, 10, 4),
            'solution_flux': (1501, 2, 10, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
            'solution_particle_partype_000': (1501, 10, 4, 4),
            'solution_particle_partype_001': (1501, 10, 4, 4),
            'solution_solid_partype_000': (1501, 10, 4, 4),
            'solution_solid_partype_001': (1501, 10, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
        },
    },
)

# %% 2D GRM
_2dgrm = Case(
    name='_2dgrm',
    model_options=_2dgrm_template,
    solution_recorder_options=no_split_options,
    expected_results={
        'last_state_y': (1228,),
        'last_state_ydot': (1228,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
            'radial_coordinates': (3,),
        },
        'solution_unit_000': {
            'last_state_y': (1212,),
            'last_state_ydot': (1212,),
            'soldot_bulk': (1501, 10, 3, 4),
            'soldot_flux': (1501, 1, 10, 3, 4),
            'soldot_inlet': (1501, 3, 4),
            'soldot_outlet': (1501, 3, 4),
            'soldot_particle': (1501, 10, 3, 4, 4),
            'soldot_solid': (1501, 10, 3, 4, 4),
            'solution_bulk': (1501, 10, 3, 4),
            'solution_flux': (1501, 1, 10, 3, 4),
            'solution_inlet': (1501, 3, 4),
            'solution_outlet': (1501, 3, 4),
            'solution_particle': (1501, 10, 3, 4, 4),
            'solution_solid': (1501, 10, 3, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
        },
    },
)

# %% 2D GRM Split Ports (single_as_multi_port=False)

_2dgrm_split_ports = Case(
    name='_2dgrm_split_ports',
    model_options=_2dgrm_template,
    solution_recorder_options=split_ports_options,
    expected_results={
        'last_state_y': (1228,),
        'last_state_ydot': (1228,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
            'radial_coordinates': (3,),
        },
        'solution_unit_000': {
            'last_state_y': (1212,),
            'last_state_ydot': (1212,),
            'soldot_bulk': (1501, 10, 3, 4),
            'soldot_flux': (1501, 1, 10, 3, 4),
            'soldot_inlet_port_000': (1501, 4),
            'soldot_inlet_port_001': (1501, 4),
            'soldot_inlet_port_002': (1501, 4),
            'soldot_outlet_port_000': (1501, 4),
            'soldot_outlet_port_001': (1501, 4),
            'soldot_outlet_port_002': (1501, 4),
            'soldot_particle': (1501, 10, 3, 4, 4),
            'soldot_solid': (1501, 10, 3, 4, 4),
            'solution_bulk': (1501, 10, 3, 4),
            'solution_flux': (1501, 1, 10, 3, 4),
            'solution_inlet_port_000': (1501, 4),
            'solution_inlet_port_001': (1501, 4),
            'solution_inlet_port_002': (1501, 4),
            'solution_outlet_port_000': (1501, 4),
            'solution_outlet_port_001': (1501, 4),
            'solution_outlet_port_002': (1501, 4),
            'solution_particle': (1501, 10, 3, 4, 4),
            'solution_solid': (1501, 10, 3, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet': (1501, 4),
            'soldot_outlet': (1501, 4),
            'solution_inlet': (1501, 4),
            'solution_outlet': (1501, 4),
        },
    },
)

# %% 2D GRM Split All

_2dgrm_split_all = Case(
    name='_2dgrm_split_all',
    model_options=_2dgrm_template,
    solution_recorder_options=split_all_options,
    expected_results={
        'last_state_y': (1228,),
        'last_state_ydot': (1228,),
        'coordinates_unit_000': {
            'axial_coordinates': (10,),
            'particle_coordinates_000': (4,),
            'radial_coordinates': (3,),
        },
        'solution_unit_000': {
            'last_state_y': (1212,),
            'last_state_ydot': (1212,),
            'soldot_bulk': (1501, 10, 3, 4),
            'soldot_flux': (1501, 1, 10, 3, 4),
            'soldot_inlet_port_000_comp_000': (1501,),
            'soldot_inlet_port_000_comp_001': (1501,),
            'soldot_inlet_port_000_comp_002': (1501,),
            'soldot_inlet_port_000_comp_003': (1501,),
            'soldot_inlet_port_001_comp_000': (1501,),
            'soldot_inlet_port_001_comp_001': (1501,),
            'soldot_inlet_port_001_comp_002': (1501,),
            'soldot_inlet_port_001_comp_003': (1501,),
            'soldot_inlet_port_002_comp_000': (1501,),
            'soldot_inlet_port_002_comp_001': (1501,),
            'soldot_inlet_port_002_comp_002': (1501,),
            'soldot_inlet_port_002_comp_003': (1501,),
            'soldot_outlet_port_000_comp_000': (1501,),
            'soldot_outlet_port_000_comp_001': (1501,),
            'soldot_outlet_port_000_comp_002': (1501,),
            'soldot_outlet_port_000_comp_003': (1501,),
            'soldot_outlet_port_001_comp_000': (1501,),
            'soldot_outlet_port_001_comp_001': (1501,),
            'soldot_outlet_port_001_comp_002': (1501,),
            'soldot_outlet_port_001_comp_003': (1501,),
            'soldot_outlet_port_002_comp_000': (1501,),
            'soldot_outlet_port_002_comp_001': (1501,),
            'soldot_outlet_port_002_comp_002': (1501,),
            'soldot_outlet_port_002_comp_003': (1501,),
            'soldot_particle': (1501, 10, 3, 4, 4),
            'soldot_solid': (1501, 10, 3, 4, 4),
            'solution_bulk': (1501, 10, 3, 4),
            'solution_flux': (1501, 1, 10, 3, 4),
            'solution_inlet_port_000_comp_000': (1501,),
            'solution_inlet_port_000_comp_001': (1501,),
            'solution_inlet_port_000_comp_002': (1501,),
            'solution_inlet_port_000_comp_003': (1501,),
            'solution_inlet_port_001_comp_000': (1501,),
            'solution_inlet_port_001_comp_001': (1501,),
            'solution_inlet_port_001_comp_002': (1501,),
            'solution_inlet_port_001_comp_003': (1501,),
            'solution_inlet_port_002_comp_000': (1501,),
            'solution_inlet_port_002_comp_001': (1501,),
            'solution_inlet_port_002_comp_002': (1501,),
            'solution_inlet_port_002_comp_003': (1501,),
            'solution_outlet_port_000_comp_000': (1501,),
            'solution_outlet_port_000_comp_001': (1501,),
            'solution_outlet_port_000_comp_002': (1501,),
            'solution_outlet_port_000_comp_003': (1501,),
            'solution_outlet_port_001_comp_000': (1501,),
            'solution_outlet_port_001_comp_001': (1501,),
            'solution_outlet_port_001_comp_002': (1501,),
            'solution_outlet_port_001_comp_003': (1501,),
            'solution_outlet_port_002_comp_000': (1501,),
            'solution_outlet_port_002_comp_001': (1501,),
            'solution_outlet_port_002_comp_002': (1501,),
            'solution_outlet_port_002_comp_003': (1501,),
            'solution_particle': (1501, 10, 3, 4, 4),
            'solution_solid': (1501, 10, 3, 4, 4),
        },
        'solution_unit_001': {
            'last_state_y': (4,),
            'last_state_ydot': (4,),
            'soldot_inlet_port_000_comp_000': (1501,),
            'soldot_inlet_port_000_comp_001': (1501,),
            'soldot_inlet_port_000_comp_002': (1501,),
            'soldot_inlet_port_000_comp_003': (1501,),
            'soldot_outlet_port_000_comp_000': (1501,),
            'soldot_outlet_port_000_comp_001': (1501,),
            'soldot_outlet_port_000_comp_002': (1501,),
            'soldot_outlet_port_000_comp_003': (1501,),
            'solution_inlet_port_000_comp_000': (1501,),
            'solution_inlet_port_000_comp_001': (1501,),
            'solution_inlet_port_000_comp_002': (1501,),
            'solution_inlet_port_000_comp_003': (1501,),
            'solution_outlet_port_000_comp_000': (1501,),
            'solution_outlet_port_000_comp_001': (1501,),
            'solution_outlet_port_000_comp_002': (1501,),
            'solution_outlet_port_000_comp_003': (1501,),
        },
    },
)

# %% Actual tests

use_dll = [False, True]
test_cases = [
    grm,
    grm_split,
    grm_sens,
    grm_par_types,
    _2dgrm,
    _2dgrm_split_ports,
    _2dgrm_split_all
]

@pytest.mark.parametrize("use_dll", use_dll)
@pytest.mark.parametrize("test_case", test_cases)
def test_simulator_options(use_dll, test_case):
    model_options = test_case.model_options
    solution_recorder_options = test_case.solution_recorder_options
    expected_results = test_case.expected_results

    model = run_simulation_with_options(
        use_dll, model_options, solution_recorder_options
    )

    assert model.root.output.last_state_y.shape == expected_results['last_state_y']
    assert model.root.output.last_state_ydot.shape == expected_results['last_state_ydot']

    for key, value in expected_results['coordinates_unit_000'].items():
        assert model.root.output.coordinates.unit_000[key].shape == value

    for key, value in expected_results['solution_unit_000'].items():
        assert model.root.output.solution.unit_000[key].shape == value

    for key, value in expected_results['solution_unit_001'].items():
        assert model.root.output.solution.unit_001[key].shape == value

    if model_options['include_sensitivity']:
        for key, value in expected_results['sens_param_000_unit_000'].items():
            assert model.root.output.sensitivity.param_000.unit_000[key].shape == value

    if model_options['include_sensitivity']:
        for key, value in expected_results['sens_param_000_unit_001'].items():
            assert model.root.output.sensitivity.param_000.unit_001[key].shape == value


if __name__ == "__main__":
    pytest.main(["test_dll.py"])
