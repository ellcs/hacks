import z3
import tabulate

def blocks(q):
    accu = []
    y = 0
    while y < 9:
        accu.append(q[y][0:3] + q[y+1][0:3] + q[y+2][0:3])
        accu.append(q[y][3:6] + q[y+1][3:6] + q[y+2][3:6])
        accu.append(q[y][6:9] + q[y+1][6:9] + q[y+2][6:9])
        y = y + 3
    return accu




q = [[5,    3,    None,   4,    None, None,   None, None, None],
     [None, None, 2,      None,    3, None,      1,    4, None],
     [9,    1,    None,   None,    2, None,   None,    3,    5],
    
     [None, 2,       6,   None,    4, None,      3, None, None],
     [   7,    4, None,   None,    1, None,   None,    9,    8],
     [None, None, None,   None, None,    7,   None,    1,    4],
    
     [None, None, None,      9,    7,    3,   None,    6, None],
     [   2, None,    9,   None,    8, None,      4, None,    3],
     [None,    5, None,      2,    6,    4,   None, None, None]]

s = z3.Solver()

# Replace Nones with symbols
for y, row in enumerate(q):
    for x, elem in enumerate(row):
        if elem == None:
            name = "({}/{})".format(y, x)
            symbol = z3.Int(name)
            s.add(z3.And(symbol > 0, symbol < 10))
            row[x] = symbol

# distinct rows
for row in q:
    s.add(z3.Distinct(*row))

# distinct columns
for column in zip(*q):
    s.add(z3.Distinct(*column))

# distinct 3x3 blocks:
b = blocks(q)
for block in blocks(q):
    s.add(z3.Distinct(*block))

print("State: {}".format(s.check()))

model = s.model()
for row in q:
    for x, elem in enumerate(row):
        if type(elem) != int:
            row[x] = model[elem]

print(tabulate.tabulate(q))
import pdb; pdb.set_trace()
