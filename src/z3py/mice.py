import z3
# Consider the following puzzle. Spend exactly 100 dollars and buy
# exactly 100 animals. Dogs cost 15 dollars, cats cost 1 dollar, and
# mice cost 25 cents each. You have to buy at least one of each. How
# many of each should you buy? 

dogs = z3.Real('dogs')
cats = z3.Real('cats')
mice = z3.Real('mice')

s = z3.Solver()

s.add(100 == ((dogs * 15) + (cats * 1) + (mice * 0.25)))
s.add(z3.And(dogs > 0, cats > 0, mice > 0))

print(s.check())
if s.check() == z3.sat:
    print(s.model())

# PROBLEM: We get half cats. Better approach: Use z3.Int and dont check for 100, but 10000.
