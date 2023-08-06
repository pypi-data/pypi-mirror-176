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
def electrical_power(solv_vars, vars, dict_val):
    P = vars[0]
    V = vars[1]
    I = vars[2]

    eq = Eq(P, V*I)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Electrical Power'
names.append(name)
vars_names[name] = ['Power', 'Tension', 'Current']
variables[name] = ['P', 'V', 'I']
formulas[name] = 'P = V*I'
num_vars[name] = 3
equations[name] = electrical_power