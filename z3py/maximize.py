from z3 import *

o = Optimize()
x = Int('x')
o.add(x > 200)
o.add(x < 900)
o.maximize(x)
o.check()
o.model()

import pdb; pdb.set_trace()
