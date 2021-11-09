import re
import angr
import claripy
import sys
import argparse


def parse_args():
    examples='''examples:

      python %s 0x000011d7 ../stdin/a.out

      python %s --base-addr 0x1 0x000011d8 ../stdin/a.out

      python %s 0x00001208 ./a.out "SOLVE(4)" "SOLVE(4)"

      python %s --avoid-addrs 0x0,0x1 0x00001208 ./a.out "SOLVE(4)" "SOLVE(4)"

      # Change the marker for symbolic argvs
      python %s --symbolic-marker SYM 0x00001208 ./a.out "SYM(4)" "SYM(4)"

      python %s 0x00001208 ./a.out -a "SOLVE(4)" -b "SOLVE(4)"

    '''
    parser = argparse.ArgumentParser(description='Symbolic solve input to reach given address.', 
                                     epilog=examples,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--symbolic-marker', dest='symbolic_marker', type=str, default="SOLVE")
    parser.add_argument('--base-addr', dest='BASE_ADDR', type=str, default="0x0")
    parser.add_argument('--avoid-addrs', dest='avoid', type=str, default="", help="Comma seperated list of addresses")
    parser.add_argument('GOOD_ADDR', type=str)
    parser.add_argument('BINARY', type=str, help="Path to executable binary")
    parser.add_argument('ARGS', type=str, nargs="*", help="ARGV for given binary. ", default=[])
    return parser.parse_args()


def make_argv_symbolic(argv, symbolic_marker):
    regex = "%s\((?P<size>\d)\)" % symbolic_marker
    for i, arg in enumerate(argv): 
        if m := re.search(regex, arg):
            size = int(m.group(1), 0)
            name = 'argv_%d' % i
            argv[i] = claripy.BVS(name, 8 * size)
    return argv


def parse_avoid_addr(s):
    accu = []
    for addr in s.split(","):
        try:
            accu.append(int(addr.strip(), 0))
        except:
            print("Couldn't parse '{}' to avoid".format(addr))
            exit(-1)
    return accu


in_args = parse_args()
binary_name = in_args.BINARY
base_addr = int(in_args.BASE_ADDR, 0)
good_addr = int(in_args.GOOD_ADDR, 0)
avoid_addrs = parse_avoid_addr(in_args.avoid)
argv      = in_args.ARGS

project = angr.Project(binary_name, load_options = { 'main_opts': {'base_addr': base_addr }})
argv = make_argv_symbolic(argv, in_args.symbolic_marker)
initial_state = project.factory.full_init_state(args=([binary_name] + argv))


simulation = project.factory.simgr(initial_state)
simulation.explore(find=good_addr, avoid=avoid_addrs)

if simulation.found:
    for solution_state in simulation.found:
        argv = [solution_state.solver.eval(arg, cast_to=bytes) for arg in argv]
        argv = [repr(str(arg, 'utf-8', 'ignore')) for arg in argv]
        print("$ > {}".format(" ".join([binary_name] + argv)))
        print("STDIN:")
        print(solution_state.posix.dumps(sys.stdin.fileno()))
else:
    raise Exception('No solution')
