from z3 import *

x = Real('x')
# prints -4
solve(x * x == 16)
# prints 4
solve(x * x == 16, x > 0)
