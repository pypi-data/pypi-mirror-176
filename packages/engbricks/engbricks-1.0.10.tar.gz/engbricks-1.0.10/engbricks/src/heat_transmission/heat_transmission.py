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
def heat_conduction(solv_vars, vars, dict_val):
    q = vars[0]
    k = vars[1]
    A = vars[2]
    delta_T = vars[3]
    delta_x = vars[4]

    eq = Eq(q, -k * A * delta_T/delta_x)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Heat Conduction'
names.append(name)
vars_names[name] = ['Heat Conduction', 'thermal conductivity', 'Area', 'Temperature Change', 'Distance Change']
variables[name] = ['q', 'k', 'A', 'delta_T', 'delta_x']
formulas[name] = 'q = -k * A * delta_T/delta_x'
num_vars[name] = 5
equations[name] = heat_conduction
# 
# 
# 
def heat_convection(solv_vars, vars, dict_val):
    q = vars[0]
    h = vars[1]
    A = vars[2]
    delta_T = vars[3]

    eq = Eq(q, h * A * delta_T)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Heat Convection'
names.append(name)
vars_names[name] = ['Heat Convection', 'Thermal Conductivity', 'Area', 'Temperature Change']
variables[name] = ['q', 'k', 'A', 'delta_T']
formulas[name] = 'q = k * A * delta_T'
num_vars[name] = 4
equations[name] = heat_convection
# 
# 
# 
def heat_radiation(solv_vars, vars, dict_val):
    q = vars[0]
    theta = vars[1]
    epsilon = vars[2]
    F_1_2 = vars[3]
    A = vars[4]
    T_s = vars[5]
    T_inf = vars[6]

    eq = Eq(q, theta * epsilon *F_1_2 * A * (T_s**4 - T_inf**4))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Heat Radiation'
names.append(name)
vars_names[name] = ['Heat Radiation', 'Stefan–Boltzmann Constant', 'View Factor','Emissivity', 'Area', 'Temp Surface', 'Temp. Inf']
variables[name] = ['q', 'theta', 'epsilon', 'F_1_2', 'A', 'T_s', 'T_inf']
formulas[name] = 'q = theta * epsilon *F_1_2 * A * (T_s**4 - T_inf**4)'
num_vars[name] = 7
equations[name] = heat_radiation
# 
# 
# 
def heat_flux(solv_vars, vars, dict_val):
    q_line = vars[0]
    q = vars[1]
    A = vars[2]

    eq = Eq(q_line, q / A)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Heat Flux'
names.append(name)
vars_names[name] = ['Heat Flux', 'Heat Conduction', 'Area']
variables[name] = ['q_line', 'q', 'A']
formulas[name] = 'q_line = q / A'
num_vars[name] = 3
equations[name] = heat_flux
# 
# 
# 
def thermal_conductivity(solv_vars, vars, dict_val):
    k = vars[0]
    c_p = vars[1]
    rho = vars[2]
    alpha = vars[3]

    eq = Eq(k, c_p * rho * alpha)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Thermal Conductivity'
names.append(name)
vars_names[name] = ['Thermal Conductivity', 'Specific heat Capacity', 'Density', 'Thermal Diffusivity']
variables[name] = ['k', 'c_p', 'rho', 'alpha']
formulas[name] = 'k = c_p * rho * alpha'
num_vars[name] = 4
equations[name] = thermal_conductivity
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