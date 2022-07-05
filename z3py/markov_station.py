from z3 import *
s = Solver()
p1 = Real('p1')
p2 = Real('p2')
p3 = Real('p3')

s.add(p1 == (p2 * (3 / 10.0) + p3 * 0.5))
s.add(p2 == (p1 * (7 / 10.0) + p2 * 0.5 + p3 * 0.5))
s.add(p3 == (p1 * (3 / 10.0) + p2 * (2 / 10.0)))
s.add(p1 + p2 + p3 == 1.0)

print(s.check())
print(s.model())
