# The eight queens puzzle is the problem of placing eight chess queens on an
# 8x8 chessboard so that no two queens attack each other. Thus, a solution
# requires that no two queens share the same row, column, or diagonal. 
import z3


s = z3.Solver()

queens = [z3.Int(i) for i in range(0, 8)]

for queen in queens:
    s.add(z3.And(queen >= 1, queen <= 8))

s.add(z3.Distinct(*queens))

for i in range(7):
    for n in range(i, 8):
        s.add(z3.Not(queens[n] - n == queens[i]))
        s.add(z3.Not(queens[n] + n == queens[i]))

print(s.check())
if s.check() == z3.sat:
    print(s.model())
import pdb; pdb.set_trace()
