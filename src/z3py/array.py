from z3 import *
s = Solver()
x = Int('x')
y = Int('y')
A = Array('A', IntSort(), IntSort())
B = Array('B', IntSort(), IntSort())

s.add(x > 100)
s.add(A[0] == 5)
s.add(A[x] == x, Store(A, x, y) == A)
s.add(B == A)

print(s.check())
print(s.model())
