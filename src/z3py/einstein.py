

green = Int('green')
blue = Int('blue')
brown = Int('brown')
red = Int('red')
yellow = Int('yellow')

s.add(And(0 < green,  green < 10))
s.add(And(0 < blue,   blue < 10))
s.add(And(0 < brown,  brown < 10))
s.add(And(0 < red,    red < 10))
s.add(And(0 < yellow, yellow < 10))

# 1
s.add(green + yellow == blue)

# 5
s.add(Distinct(green, blue, brown, red, yellow))

# 6
s.add(green == 6)

# 7
s.add(yellow + 4 == brown)




