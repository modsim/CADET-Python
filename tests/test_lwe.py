# Normally the main function is placed at the bottom of the file, but I have placed it at the top so that
# This interface is more like a tutorial and can be read from the top down and any given function
# can be drilled into to learn more about it.
import os

import matplotlib.pyplot as plt
import numpy

from cadet import Cadet
from tests import common


# Helper functions that make it easier to set the values in the HDF5 file
# In the CADET pdf file each value in the hdf5 file has a type. The functions
# below match those types.

def main():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    simulation = Cadet(common.common.root)
    simulation.filename = "tmp/LWE.h5"
    createSimulation(simulation)
    simulation.save()
    simulation.run()
    simulation.load()

    plotSimulation(simulation)
    return simulation


def createSimulation(simulation):
    root = simulation.root

    root.input.model.nunits = 3
    root.input.model.unit_001.discretization.use_analytic_jacobian = 1

    root.input.model.connections.nswitches = 1
    root.input.model.connections.switch_000.section = 0
    root.input.model.connections.switch_000.connections = [0, 1, -1, -1, 1.0,
                                                           1, 2, -1, -1, 1.0]
    root.input.model.unit_000.inlet_type = 'PIECEWISE_CUBIC_POLY'
    root.input.model.unit_000.unit_type = 'INLET'
    root.input.model.unit_000.ncomp = 2

    root.input.model.unit_000.sec_000.const_coeff = [50.0, 1.0]
    root.input.model.unit_000.sec_000.lin_coeff = [0.0, 0.0]
    root.input.model.unit_000.sec_000.quad_coeff = [0.0, 0.0]
    root.input.model.unit_000.sec_000.cube_coeff = [0.0, 0.0]

    root.input.model.unit_000.sec_001.const_coeff = [50.0, 0.0]
    root.input.model.unit_000.sec_001.lin_coeff = [0.0, 0.0]
    root.input.model.unit_000.sec_001.quad_coeff = [0.0, 0.0]
    root.input.model.unit_000.sec_001.cube_coeff = [0.0, 0.0]

    root.input.model.unit_000.sec_002.const_coeff = [100.0, 0.0]
    root.input.model.unit_000.sec_002.lin_coeff = [0.2, 0.0]
    root.input.model.unit_000.sec_002.quad_coeff = [0.0, 0.0]
    root.input.model.unit_000.sec_002.cube_coeff = [0.0, 0.0]

    root.input.model.unit_001.adsorption_model = 'STERIC_MASS_ACTION'
    root.input.model.unit_001.col_dispersion = 5.75e-8
    root.input.model.unit_001.col_length = 0.014
    root.input.model.unit_001.col_porosity = 0.37
    root.input.model.unit_001.film_diffusion = [6.9e-6, 6.9e-6]
    root.input.model.unit_001.init_c = [50.0, 0.0]
    root.input.model.unit_001.init_q = [1200.0, 0.0]
    root.input.model.unit_001.ncomp = 2
    root.input.model.unit_001.par_diffusion = [7e-10, 6.07e-11]
    root.input.model.unit_001.par_porosity = 0.75
    root.input.model.unit_001.par_radius = 4.5e-5
    root.input.model.unit_001.par_surfdiffusion = [0.0, 0.0]
    root.input.model.unit_001.unit_type = 'GENERAL_RATE_MODEL'

    # root.input.model.unit_001.velocity = 1
    # root.input.model.unit_001.cross_section_area = 4700.352526439483
    root.input.model.unit_001.velocity = 5.75e-4

    root.input.model.unit_001.adsorption.is_kinetic = 0
    root.input.model.unit_001.adsorption.sma_ka = [0.0, 35.5]
    root.input.model.unit_001.adsorption.sma_kd = [0.0, 1000.0]
    root.input.model.unit_001.adsorption.sma_lambda = 1200.0
    root.input.model.unit_001.adsorption.sma_nu = [0.0, 4.7]
    root.input.model.unit_001.adsorption.sma_sigma = [0.0, 11.83]

    root.input.model.unit_001.discretization.nbound = [1, 1]
    root.input.model.unit_001.discretization.ncol = 100
    root.input.model.unit_001.discretization.npar = 5

    root.input.model.unit_002.ncomp = 2
    root.input.model.unit_002.unit_type = 'OUTLET'

    root.input.solver.user_solution_times = numpy.linspace(0, 1500, 1500)
    root.input.solver.sections.nsec = 3
    root.input.solver.sections.section_continuity = [0, 0]
    root.input.solver.sections.section_times = [0.0, 10.0, 90.0, 1500.0]


def plotSimulation(simulation):
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=[16, 8])
    plotInlet(ax1, simulation)
    plotOutlet(ax2, simulation)
    f.tight_layout()
    plt.savefig("tmp/lwe.png")


def plotInlet(axis, simulation):
    solution_times = simulation.root.output.solution.solution_times

    inlet_salt = simulation.root.output.solution.unit_000.solution_inlet_comp_000
    inlet_p1 = simulation.root.output.solution.unit_000.solution_inlet_comp_001
    # inlet_p2 = simulation.root.output.solution.unit_000.solution_inlet_comp_002
    # inlet_p3 = simulation.root.output.solution.unit_000.solution_inlet_comp_003

    axis.set_title("Inlet")
    axis.plot(solution_times, inlet_salt, 'b-', label="Salt")
    axis.set_xlabel('time (s)')

    # Make the y-axis label, ticks and tick labels match the line color.
    axis.set_ylabel('mMol Salt', color='b')
    axis.tick_params('y', colors='b')

    axis2 = axis.twinx()
    axis2.plot(solution_times, inlet_p1, 'r-', label="P1")
    # axis2.plot(solution_times, inlet_p2, 'g-', label="P2")
    # axis2.plot(solution_times, inlet_p3, 'k-', label="P3")
    axis2.set_ylabel('mMol Protein', color='r')
    axis2.tick_params('y', colors='r')

    lines, labels = axis.get_legend_handles_labels()
    lines2, labels2 = axis2.get_legend_handles_labels()
    axis2.legend(lines + lines2, labels + labels2, loc=0)


def plotOutlet(axis, simulation):
    solution_times = simulation.root.output.solution.solution_times

    outlet_salt = simulation.root.output.solution.unit_002.solution_outlet_comp_000
    outlet_p1 = simulation.root.output.solution.unit_002.solution_outlet_comp_001
    # outlet_p2 = simulation.root.output.solution.unit_002.solution_outlet_comp_002
    # outlet_p3 = simulation.root.output.solution.unit_002.solution_outlet_comp_003

    axis.set_title("Output")
    axis.plot(solution_times, outlet_salt, 'b-', label="Salt")
    axis.set_xlabel('time (s)')

    # Make the y-axis label, ticks and tick labels match the line color.
    axis.set_ylabel('mMol Salt', color='b')
    axis.tick_params('y', colors='b')

    axis2 = axis.twinx()
    axis2.plot(solution_times, outlet_p1, 'r-', label="P1")
    # axis2.plot(solution_times, outlet_p2, 'g-', label="P2")
    # axis2.plot(solution_times, outlet_p3, 'k-', label="P3")
    axis2.set_ylabel('mMol Protein', color='r')
    axis2.tick_params('y', colors='r')

    lines, labels = axis.get_legend_handles_labels()
    lines2, labels2 = axis2.get_legend_handles_labels()
    axis2.legend(lines + lines2, labels + labels2, loc=0)


def test_lwe():
    sim = main()
    assert isinstance(sim.root.output.solution.unit_002.solution_outlet_comp_001, numpy.ndarray)
    assert isinstance(sim.root.output.solution.unit_002.solution_outlet_comp_000, numpy.ndarray)
