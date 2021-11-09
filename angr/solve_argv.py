import angr
import claripy
import sys

binary_name = "./a.out"
base_addr   = 0x0
good_addr   = 0x00001208
avoid_addr  = []

project = angr.Project(binary_name, load_options = { 'main_opts': {'base_addr': base_addr }})

argv1 = claripy.BVS('argv1', 8 * 0x4)
argv2 = claripy.BVS('argv2', 8 * 0x4)

initial_state = project.factory.entry_state(args=[binary_name, argv1, argv2])

simulation = project.factory.simgr(initial_state)
simulation.explore(find=good_addr, avoid_addr=[])

if simulation.found:
     solution_state = simulation.found[0]
     argv1 = solution_state.solver.eval(argv1, cast_to=bytes)
     argv2 = solution_state.solver.eval(argv2, cast_to=bytes)
     print(argv1)
     print(argv2)
else:
    raise Exception('No solution')
