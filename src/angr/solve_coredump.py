import cle
import angr
import claripy


# Set the reg values from the elfcore_object to the sim state, realizing that not all
# of the registers will be supported (particularly some segment registers)
# for regname, regval in elfcore_object.thread_registers():
def fixed_elfcore_project(filename):
    project = angr.Project(filename, main_opts={'backend': 'elfcore'})
    initial_state = project.factory.full_init_state()

    # Get the elfcore_object
    elfcore_object = None
    for obj in project.loader.all_objects:
        if type(obj) == cle.backends.elf.elfcore.ELFCore:
            elfcore_object = obj
            break

    if elfcore_object is None:
        error
    
    regs = elfcore_object.thread_registers()
    initial_state.regs.rax = regs['rax']
    initial_state.regs.rcx = regs['rcx']
    initial_state.regs.rdx = regs['rdx']
    initial_state.regs.rbx = regs['rbx']
    initial_state.regs.rsp = regs['rsp']
    initial_state.regs.rbp = regs['rbp']
    initial_state.regs.rsi = regs['rsi']
    initial_state.regs.rdi = regs['rdi']
    initial_state.regs.r8  = regs['r8']
    initial_state.regs.r9  = regs['r9']
    initial_state.regs.r10 = regs['r10']
    initial_state.regs.r11 = regs['r11']
    initial_state.regs.r12 = regs['r12']
    initial_state.regs.r13 = regs['r13']
    initial_state.regs.r14 = regs['r14']
    initial_state.regs.r15 = regs['r15']
    initial_state.regs.rip = regs['rip']
    print("rip: %x" % regs['rip'])
    return project, initial_state

project, initial_state = fixed_elfcore_project("core.430068")
MAX_FLAG_LEN = 26

# since rust doesn't terminate their strings with a \0, but holds the length
# of a string within the registers, we have to make that string-length symbolic
# aswell.
flag_len = claripy.BVS('flag_len', 64)
initial_state.regs.rbx = flag_len
initial_state.solver.add(flag_len <= MAX_FLAG_LEN)

# we can only type printable characters into the GUI.
# the address to the flag is stored within the register r14.
flag = claripy.BVS('flag', MAX_FLAG_LEN * 8)
for c in flag.chop(0x8):
    initial_state.solver.add(c <= '~')
    initial_state.solver.add(c >= ' ')
initial_state.memory.store(initial_state.regs.r14, flag)


simulation = project.factory.simgr(initial_state)

good_addr=0x55df6050908b
bad_addr =0x55df60509075
simulation.explore(find=good_addr, avoid=bad_addr)

if simulation.found:
    solution_state = simulation.found[0]
    print("Length: {}".format(solution_state.solver.eval(flag_len, cast_to=bytes)))
    print(solution_state.solver.eval(flag, cast_to=bytes))
else:
    print("No solution found")

