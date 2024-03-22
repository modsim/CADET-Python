import os

import matplotlib.pyplot as plt
import numpy
import pandas
import pytest

from cadet import Cadet
from tests import common


def gen_fraction_times(start, stop, bins):
    return numpy.linspace(start, stop, bins + 1, endpoint=True)


def gen_fractions(fraction_times, sim):
    nComp = sim.root.input.model.unit_000.ncomp

    df = pandas.DataFrame()

    times = sim.root.output.solution.solution_times

    for idx, (start, stop) in enumerate(zip(fraction_times[:-1], fraction_times[1:])):
        selected = (times >= start) & (times <= stop)
        temp = {'Start': start, 'Stop': stop}
        for comp in range(nComp):
            local_times = times[selected]
            local_values = sim.root.output.solution.unit_001["solution_outlet_comp_%03d" % comp][selected]

            temp[str(comp)] = numpy.trapz(local_values, local_times) / (stop - start)
        df = df.append(temp, ignore_index=True)
    return df


def main():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    simulation = Cadet(common.common.root)
    simulation.filename = "tmp/MSSMA_2comp.h5"
    createSimulation(simulation)
    simulation.save()
    data = simulation.run()
    print(data)
    simulation.load()
    plotSimulation(simulation)
    return simulation


def createSimulation(simulation):
    root = simulation.root

    root.input.model.nunits = 3

    root.input.model.connections.nswitches = 1
    root.input.model.connections.switch_000.section = 0
    root.input.model.connections.switch_000.connections = [0, 1, -1, -1, 1.0,
                                                           1, 2, -1, -1, 1.0]
    root.input.model.unit_000.inlet_type = 'PIECEWISE_CUBIC_POLY'
    root.input.model.unit_000.unit_type = 'INLET'
    root.input.model.unit_000.ncomp = 3

    root.input.model.unit_000.sec_000.const_coeff = [100.0, 0.15, 0.01]
    root.input.model.unit_000.sec_000.lin_coeff = [0.0, 0.0, 0.0]
    root.input.model.unit_000.sec_000.quad_coeff = [0.0, 0.0, 0.0]
    root.input.model.unit_000.sec_000.cube_coeff = [0.0, 0.0, 0.0]

    root.input.model.unit_000.sec_001.const_coeff = [75, 0.0, 0.0]
    root.input.model.unit_000.sec_001.lin_coeff = [0.0, 0.0, 0.0]
    root.input.model.unit_000.sec_001.quad_coeff = [0.0, 0.0, 0.0]
    root.input.model.unit_000.sec_001.cube_coeff = [0.0, 0.0, 0.0]

    root.input.model.unit_000.sec_002.const_coeff = [75, 0.0, 0.0]
    root.input.model.unit_000.sec_002.lin_coeff = [0.05, 0.0, 0.0]
    root.input.model.unit_000.sec_002.quad_coeff = [0.0, 0.0, 0.0]
    root.input.model.unit_000.sec_002.cube_coeff = [0.0, 0.0, 0.0]

    root.input.model.unit_001.adsorption_model = 'MULTISTATE_STERIC_MASS_ACTION'
    root.input.model.unit_001.col_dispersion = 1.5E-7
    root.input.model.unit_001.col_length = 0.25
    root.input.model.unit_001.col_porosity = 0.3
    root.input.model.unit_001.film_diffusion = [2.14E-4, 2.1e-5, 2.1e-5]
    root.input.model.unit_001.init_c = [75, 0.0, 0.0]
    root.input.model.unit_001.init_q = [225, 0.0, 0.0, 0.0, 0.0]
    root.input.model.unit_001.ncomp = 3
    root.input.model.unit_001.par_diffusion = [4.08E-10, 9.0E-12, 9.0e-12]
    root.input.model.unit_001.par_porosity = 0.4
    root.input.model.unit_001.par_radius = 3.25E-5
    root.input.model.unit_001.par_surfdiffusion = [0.0, 0.0, 0.0, 0.0, 0.0]
    root.input.model.unit_001.unit_type = 'GENERAL_RATE_MODEL'
    root.input.model.unit_001.velocity = 0.001

    root.input.model.unit_001.adsorption.is_kinetic = 1
    root.input.model.unit_001.adsorption.mssma_ka = [0.0, 1E11, 8E6, 1E11, 8E6]
    root.input.model.unit_001.adsorption.mssma_kd = [0.0, 6E11, 2E16, 6E11, 2E16]
    root.input.model.unit_001.adsorption.mssma_lambda = 225
    root.input.model.unit_001.adsorption.mssma_nu = [0.0, 10, 25, 20, 50]
    root.input.model.unit_001.adsorption.mssma_sigma = [0.0, 48, 66, 48 * 2, 66 * 2]
    root.input.model.unit_001.adsorption.mssma_refq = 225
    root.input.model.unit_001.adsorption.mssma_refc0 = 520.0
    root.input.model.unit_001.adsorption.mssma_rates = [0.0, 0.0, 1e20, 10, 0.0, 0.0, 1e20, 10, 0.0]

    root.input.model.unit_001.discretization.nbound = [1, 2, 2]
    root.input.model.unit_001.discretization.ncol = 50
    root.input.model.unit_001.discretization.npar = 5

    root.input.model.unit_002.ncomp = 3
    root.input.model.unit_002.unit_type = 'OUTLET'

    root.input.solver.user_solution_times = numpy.linspace(0, 15000, 1000)
    root.input.solver.sections.nsec = 3
    root.input.solver.sections.section_continuity = [0, 0]
    root.input.solver.sections.section_times = [0.0, 4500, 6100, 15000]

    root.input.solver.consistent_init_mode = 3


def plotSimulation(simulation):
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=[16, 8])
    plotInlet(ax1, simulation)
    plotOutlet(ax2, simulation)
    f.tight_layout()
    plt.savefig("tmp/MSSMA.png")


def plotInlet(axis, simulation):
    solution_times = simulation.root.output.solution.solution_times

    inlet_salt = simulation.root.output.solution.unit_000.solution_inlet_comp_000
    inlet_p1 = simulation.root.output.solution.unit_000.solution_inlet_comp_001
    inlet_p2 = simulation.root.output.solution.unit_000.solution_inlet_comp_002

    axis.set_title("Inlet")
    axis.plot(solution_times, inlet_salt, 'b-', label="Salt")
    axis.set_xlabel('time (s)')

    # Make the y-axis label, ticks and tick labels match the line color.
    axis.set_ylabel('mMol Salt', color='b')
    axis.tick_params('y', colors='b')

    axis2 = axis.twinx()
    axis2.plot(solution_times, inlet_p1, 'r-', label="P1")
    axis2.plot(solution_times, inlet_p2, 'g-', label="P2")
    axis2.set_ylabel('mMol Protein', color='r')
    axis2.tick_params('y', colors='r')

    lines, labels = axis.get_legend_handles_labels()
    lines2, labels2 = axis2.get_legend_handles_labels()
    axis2.legend(lines + lines2, labels + labels2, loc=0)


def plotOutlet(axis, simulation):
    solution_times = simulation.root.output.solution.solution_times

    outlet_salt = simulation.root.output.solution.unit_002.solution_outlet_comp_000
    outlet_p1 = simulation.root.output.solution.unit_002.solution_outlet_comp_001
    outlet_p2 = simulation.root.output.solution.unit_002.solution_outlet_comp_002

    data = numpy.vstack([solution_times, outlet_p1]).transpose()
    numpy.savetxt('tmp/comp2_1.csv', data, delimiter=',')

    data = numpy.vstack([solution_times, outlet_p2]).transpose()
    numpy.savetxt('tmp/comp2_2.csv', data, delimiter=',')

    data = numpy.vstack([solution_times, outlet_p1 + outlet_p2]).transpose()
    numpy.savetxt('tmp/comp2_comb.csv', data, delimiter=',')

    fraction_times = gen_fraction_times(6000, 14000, 10)
    df = gen_fractions(fraction_times, simulation)
    df.to_csv("tmp/comp2_fraction.csv", columns=('Start', 'Stop', '1'), index=False)

    axis.set_title("Output")
    axis.plot(solution_times, outlet_salt, 'b-', label="Salt")
    axis.set_xlabel('time (s)')

    # Make the y-axis label, ticks and tick labels match the line color.
    axis.set_ylabel('mMol Salt', color='b')
    axis.tick_params('y', colors='b')

    axis2 = axis.twinx()
    axis2.plot(solution_times, outlet_p1, 'r-', label="P1")
    axis2.plot(solution_times, outlet_p2, 'g-', label="P2")
    axis2.set_ylabel('mMol Protein', color='r')
    axis2.tick_params('y', colors='r')

    lines, labels = axis.get_legend_handles_labels()
    lines2, labels2 = axis2.get_legend_handles_labels()
    axis2.legend(lines + lines2, labels + labels2, loc=0)


@pytest.mark.slow
def test_MSSMA_2comp():
    sim = main()
    assert isinstance(sim.root.output.solution.unit_002.solution_outlet_comp_001, numpy.ndarray)
    assert isinstance(sim.root.output.solution.unit_002.solution_outlet_comp_000, numpy.ndarray)


if __name__ == "__main__":
    import sys

    print(sys.version)
    main()
