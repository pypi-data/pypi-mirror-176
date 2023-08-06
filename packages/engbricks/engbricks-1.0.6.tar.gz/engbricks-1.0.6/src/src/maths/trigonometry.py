from sympy import Eq, solve
from sympy import sin, cos, tan, atan, ln, pi, sqrt
# 
# 
# 
names = []
vars_names = {}
variables = {}
formulas = {}
num_vars = {}
equations = {}
# 
# 
# 
def sine(solv_vars, vars, dict_val):
    sin_B = vars[0]
    b = vars[1]
    a = vars[2]

    eq = Eq(sin_B, b/a)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Sine'
names.append(name)
vars_names[name] = ['sin(B)', 'Opposite Side', 'Hypotenuse']
variables[name] = ['sin_B', 'b', 'a']
formulas[name] = 'sin(B) = b/a'
num_vars[name] = 3
equations[name] = sine
# 
# 
# 
def cosine(solv_vars, vars, dict_val):
    cos_B = vars[0]
    c = vars[1]
    a = vars[2]

    eq = Eq(cos_B, c/a)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Cosine'
names.append(name)
vars_names[name] = ['cos(B)', 'Adjacent Side', 'Hypotenuse']
variables[name] = ['cos_B', 'c', 'a']
formulas[name] = 'cos(B) = c/a'
num_vars[name] = 3
equations[name] = cosine
# 
# 
# 
def law_of_sines(solv_vars, vars, dict_val):
    a = vars[0]
    b = vars[1]
    A = vars[2]
    B = vars[3]

    eq = Eq(a / sin(A), b / sin(B))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Law of Sines'
names.append(name)
vars_names[name] = ['Side', 'Other Side', 'Angle', 'Other Angle']
variables[name] = ['a', 'b', 'A', 'B']
formulas[name] = 'a / sin(A) = b / sin(B)'
num_vars[name] = 4
equations[name] = law_of_sines
# 
# 
# 
def law_of_cosines(solv_vars, vars, dict_val):
    a = vars[0]
    b = vars[1]
    c = vars[2]
    C = vars[3]

    eq = Eq(c**2, a**2 + b**2 - 2 * a * b * cos(C))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Law of Cosines'
names.append(name)
vars_names[name] = ['Hypotenuse', 'Adjacent Side', 'Opposite Side', 'Angle']
variables[name] = ['a', 'b', 'c', 'C']
formulas[name] = 'c**2 = a**2 + b**2 - 2 * a * b * cos(C)'
num_vars[name] = 4
equations[name] = law_of_cosines
# 
# 
# 
def law_of_tangents(solv_vars, vars, dict_val):
    a = vars[0]
    b = vars[1]
    A = vars[2]
    B = vars[3]

    eq = Eq((a + b) / (a - b), tan(1/2*(A + B)) / tan(1/2*(A - B)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Law of Tangents'
names.append(name)
vars_names[name] = ['Side', 'Other Side', 'Angle', 'Other Angle']
variables[name] = ['a', 'b', 'A', 'B']
formulas[name] = '(a + b) / (a - b) = tan(1/2*(A + B)) / tan(1/2*(A - B))'
num_vars[name] = 4
equations[name] = law_of_tangents