from cadet import Cadet

common = Cadet()

root = common.root

root.input.model.solver.gs_type = 1
root.input.model.solver.max_krylov = 0
root.input.model.solver.max_restarts = 10
root.input.model.solver.schur_safety = 1e-8

# CADET 3.1 and CADET-dev flags are in here so that it works with both
root.input['return'].write_solution_times = 1
root.input['return'].split_components_data = 1
root.input['return'].unit_000.write_sens_bulk = 0
root.input['return'].unit_000.write_sens_flux = 0
root.input['return'].unit_000.write_sens_inlet = 1
root.input['return'].unit_000.write_sens_outlet = 1
root.input['return'].unit_000.write_sens_particle = 0
root.input['return'].unit_000.write_solution_bulk = 0
root.input['return'].unit_000.write_solution_flux = 0
root.input['return'].unit_000.write_solution_inlet = 1
root.input['return'].unit_000.write_solution_outlet = 1
root.input['return'].unit_000.write_solution_particle = 0
root.input['return'].unit_000.write_sens_column = 0
root.input['return'].unit_000.write_sens_column_inlet = 1
root.input['return'].unit_000.write_sens_column_outlet = 1
root.input['return'].unit_000.write_solution_column = 0
root.input['return'].unit_000.write_solution_column_inlet = 1
root.input['return'].unit_000.write_solution_column_outlet = 1

root.input['return'].unit_001 = root.input['return'].unit_000
root.input['return'].unit_002 = root.input['return'].unit_000

root.input.model.unit_001.discretization.par_disc_type = 'EQUIDISTANT_PAR'
root.input.model.unit_001.discretization.schur_safety = 1.0e-8
root.input.model.unit_001.discretization.use_analytic_jacobian = 1
root.input.model.unit_001.discretization.weno.boundary_model = 0
root.input.model.unit_001.discretization.weno.weno_eps = 1e-10
root.input.model.unit_001.discretization.weno.weno_order = 3
root.input.model.unit_001.discretization.gs_type = 1
root.input.model.unit_001.discretization.max_krylov = 0
root.input.model.unit_001.discretization.max_restarts = 10

root.input.solver.time_integrator.abstol = 1e-10
root.input.solver.time_integrator.algtol = 1e-12
root.input.solver.time_integrator.init_step_size = 1e-6
root.input.solver.time_integrator.max_steps = 1000000
root.input.solver.time_integrator.reltol = 1e-10

root.input.solver.nthreads = 0
