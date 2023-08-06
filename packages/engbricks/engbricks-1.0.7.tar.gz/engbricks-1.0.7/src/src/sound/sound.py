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
def acoustic_electrical_power(solv_vars, vars, dict_val):
    J = vars[0]
    p = vars[1]
    v = vars[2]

    eq = Eq(J, p*v)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Acoustic Electrical Power'
names.append(name)
vars_names[name] = ['Intensity', 'Pressure', 'Velocity']
variables[name] = ['J', 'p', 'v']
formulas[name] = 'J = p*v'
num_vars[name] = 3
equations[name] = acoustic_electrical_power
# 
# 
# 
def acoustic_ohms_law(solv_vars, vars, dict_val):
    p = vars[0]
    v = vars[1]
    Z_0 = vars[2]

    eq = Eq(p, v*Z_0)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Acoustic Ohms Law'
names.append(name)
vars_names[name] = ['Pressure', 'Velocity', 'Acoustic Impedance']
variables[name] = ['p', 'v', 'Z_0']
formulas[name] = 'p = v*Z_0'
num_vars[name] = 3
equations[name] = acoustic_ohms_law
# 
# 
# 
def acoustic_impedance(solv_vars, vars, dict_val):
    Z_0 = vars[0]
    p = vars[1]
    c = vars[2]

    eq = Eq(Z_0, p*c)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Acoustic Impedance'
names.append(name)
vars_names[name] = ['Acoustic Impedance', 'Pressure', 'Speed of Sound']
variables[name] = ['Z_0', 'p', 'c']
formulas[name] = 'Z_0 = p*c'
num_vars[name] = 3
equations[name] = acoustic_impedance
# 
# 
# 