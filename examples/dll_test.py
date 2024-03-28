"""
On Windows: $CADET_ROOT/bin/cadet.dll
On Linux:
    release: $CADET_ROOT/lib/libcadet.so
    debug: $CADET_ROOT/lib/libcadet_d.so
"""
import copy
import os
from pathlib import Path
import platform
import subprocess
import sys
sys.path.insert(0, '../')
import tempfile

from cadet import Cadet

# cadet_root = Path(r"C:\Users\kosh\cadet_build\CADET\VCPKG_42_dll\bin\cadet.dll")
cadet_root = Path('/home/jo/code/CADET/install/capi/')

cadet_dll_path = cadet_root / 'lib' / 'libcadet_d.so'
cadet_cli_path = cadet_root / 'bin' / 'cadet-cli'

# %%

def setup_template_model(
        cadet_root,
        model='GENERAL_RATE_MODEL',
        n_partypes=1,
        include_sensitivity=False,
        file_name='LWE.h5',
        ):

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

    template = Cadet()
    template.filename = file_name
    template.load()

    return template


def setup_solution_recorder(
        template,
        split_components=0,
        split_ports=0,
        single_as_multi_port=0,
        ):

    template = copy.deepcopy(template)

    template.root.input['return'].write_solution_last = 1
    template.root.input['return'].write_sens_last = 1

    template.root.input['return'].split_components_data = split_components
    template.root.input['return'].split_ports_data = split_ports
    template.root.input['return'].single_as_multi_port = single_as_multi_port

    template.root.input['return'].unit_000.write_coordinates = 1

    template.root.input['return'].unit_000.write_solution_inlet = 1
    template.root.input['return'].unit_000.write_solution_outlet = 1
    template.root.input['return'].unit_000.write_solution_bulk = 1
    template.root.input['return'].unit_000.write_solution_particle = 1
    template.root.input['return'].unit_000.write_solution_solid = 1
    template.root.input['return'].unit_000.write_solution_flux = 1
    template.root.input['return'].unit_000.write_solution_volume = 1

    template.root.input['return'].unit_000.write_soldot_inlet = 1
    template.root.input['return'].unit_000.write_soldot_outlet = 1
    template.root.input['return'].unit_000.write_soldot_bulk = 1
    template.root.input['return'].unit_000.write_soldot_particle = 1
    template.root.input['return'].unit_000.write_soldot_solid = 1
    template.root.input['return'].unit_000.write_soldot_flux = 1
    template.root.input['return'].unit_000.write_soldot_volume = 1

    template.root.input['return'].unit_000.write_sens_inlet = 1
    template.root.input['return'].unit_000.write_sens_outlet = 1
    template.root.input['return'].unit_000.write_sens_bulk = 1
    template.root.input['return'].unit_000.write_sens_particle = 1
    template.root.input['return'].unit_000.write_sens_solid = 1
    template.root.input['return'].unit_000.write_sens_flux = 1
    template.root.input['return'].unit_000.write_sens_volume = 1

    template.root.input['return'].unit_000.write_sensdot_inlet = 1
    template.root.input['return'].unit_000.write_sensdot_outlet = 1
    template.root.input['return'].unit_000.write_sensdot_bulk = 1
    template.root.input['return'].unit_000.write_sensdot_particle = 1
    template.root.input['return'].unit_000.write_sensdot_solid = 1
    template.root.input['return'].unit_000.write_sensdot_flux = 1
    template.root.input['return'].unit_000.write_sensdot_volume = 1

    template.root.input['return'].unit_000.write_solution_last_unit = 1
    template.root.input['return'].unit_000.write_soldot_last_unit = 1

    # LAST_STATE_Y
    # LAST_STATE_YDOT
    # LAST_STATE_SENSYDOT_???
    # LAST_STATE_SENSY_???

    for unit in range(template.root.input.model['nunits']):
        template.root.input['return']['unit_{0:03d}'.format(unit)] = template.root.input['return'].unit_000

    if template.filename is not None:
        template.save()

    return template


# %%
dll = True

if dll:
    cadet_path = cadet_dll_path
else:
    cadet_path = cadet_cli_path

Cadet.cadet_path = cadet_path.as_posix()

# %% Test standard GRM
model = 'GENERAL_RATE_MODEL'

template = setup_template_model(
    cadet_root,
    model,
)

# Don't split anything
sim = setup_solution_recorder(
    template,
    split_components=0,
    split_ports=0,
    single_as_multi_port=0,
)

sim.run_load()

# Split everything
sim = setup_solution_recorder(
    template,
    split_components=1,
    split_ports=1,
    single_as_multi_port=1,
)

sim.run_load()

# %% Test sensitivities
model = 'GENERAL_RATE_MODEL'

template = setup_template_model(
    cadet_root,
    model,
    include_sensitivity=True,
)

# Don't split anything
sim = setup_solution_recorder(
    template,
    split_components=0,
    split_ports=0,
    single_as_multi_port=0,
)

sim.run_load()

# Split everything
sim = setup_solution_recorder(
    template,
    split_components=1,
    split_ports=1,
    single_as_multi_port=1,
)

sim.run_load()


# %% Test ports
model = 'GENERAL_RATE_MODEL_2D'

template = setup_template_model(cadet_root, model)
setup_solution_recorder(
    template,
    split_components=0,
    split_ports=0,
    single_as_multi_port=0,
)

sim.run_load()

# Only split ports for 2D Model
setup_solution_recorder(
    template,
    split_components=0,
    split_ports=1,
    single_as_multi_port=0,
)

# Split everything
setup_solution_recorder(
    template,
    split_components=1,
    split_ports=1,
    single_as_multi_port=1,
)

sim.run_load()
