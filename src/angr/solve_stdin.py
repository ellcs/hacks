import angr
import sys
import claripy

binary_name = './a.out'
base_addr   = 0x0
good_addr   = 0x000011d7
avoid_addrs  = []

project = angr.Project(binary_name, load_options = { 'main_opts': {'base_addr': base_addr }})

print("Entry: %x" % project.loader.main_object.entry)
initial_state = project.factory.entry_state()
simulation = project.factory.simgr(initial_state)
simulation.explore(find=good_addr, avoid=avoid_addrs)

if simulation.found:
    solution_state = simulation.found[0]
    print(solution_state.posix.dumps(sys.stdin.fileno()))
else:
    raise Exception('No solution')
