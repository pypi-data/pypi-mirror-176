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
def heat_energy(solv_vars, vars, dict_val):
    Q = vars[0]
    m = vars[1]
    c_p = vars[2]
    delta_T = vars[3]

    eq = Eq(Q, m * c_p * delta_T)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Heat Energy'
names.append(name)
vars_names[name] = ['Heat Energy', 'mass', 'Specific Heat Capacity', 'Temperature Change']
variables[name] = ['Q', 'm', 'c_p', 'delta_T']
formulas[name] = 'Q = m * c_p * delta_T'
num_vars[name] = 4
equations[name] = heat_energy
# 
# 
# 
def enthalpy(solv_vars, vars, dict_val):
    H = vars[0]
    E = vars[1]
    p = vars[2]
    V = vars[3]

    eq = Eq(H, E + p * V)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Enthalpy'
names.append(name)
vars_names[name] = ['Enthalpy', 'Internal Energy', 'Pressure', 'Volume']
variables[name] = ['H', 'E', 'p', 'V']
formulas[name] = 'H = E + p * V'
num_vars[name] = 4
equations[name] = enthalpy
# 
# 
# 
def simplified_mayer_relation(solv_vars, vars, dict_val):
    c_p = vars[0]
    c_v = vars[1]
    R = vars[2]

    eq = Eq(R, c_p - c_v)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Simplified Mayer\'s Relation'
names.append(name)
vars_names[name] = ['Gas constant', 'Specific Heat Cnt Pressure', 'Specific Heat Cnt Volume']
variables[name] = ['R', 'c_p', 'c_v']
formulas[name] = 'R = c_p - c_v'
num_vars[name] = len(variables[name])
equations[name] = simplified_mayer_relation
# 
# 
# 




# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(aaa, aaa/aaa)

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = 'aaa = aaa/aaa'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 