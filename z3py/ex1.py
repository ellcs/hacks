# Exercise 1
#
# Using Z3, determine if the following formulae are true:
# (a) ¬(x ∨ y ) ≡ (¬ x ∧ ¬ y)
# (b) (x ∧ y) ≡ ¬ (¬ x ∨ ¬ y)
#
# http://lim.univ-reunion.fr/staff/fred/Enseignement/AlgoAvancee/Exos/Z3-exercises.pdf
from z3 import *

s = Solver()
x = Bool('x')
y = Bool('y')
s.add(Not(Or(x, y)) == And(Not(x), Not(y)))

if s.check() == z3.sat:
    model = s.model()
    import pdb; pdb.set_trace()
