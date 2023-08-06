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
# 
# 
# 
def ohms_law(solv_vars, vars, dict_val):
    I = vars[0]
    V = vars[1]
    R = vars[2]

    eq = Eq(I, V/R)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Ohm\'s Law'
names.append(name)
vars_names[name] = ['Current', 'Tension', 'Resistance']
variables[name] = ['I', 'V', 'R']
formulas[name] = 'I = V/R'
num_vars[name] = 3
equations[name] = ohms_law
# 
# 
# 
import sympy as sym
import math
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
def power_factor_1(solv_vars, vars, dict_val):
    PF = vars[0]
    phi = vars[1]

    eq = Eq(PF, cos(phi))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Power Factor 1'
names.append(name)
vars_names[name] = ['Power Factor', 'Angle', 'Current']
variables[name] = ['PF', 'phi']
formulas[name] = 'PF = cos(phi)'
num_vars[name] = 2
equations[name] = power_factor_1
# 
# 
# 
def power_factor_2(solv_vars, vars, dict_val):
    PF = vars[0]
    P = vars[1]
    S = vars[2]

    eq = Eq(PF, P/S)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Power Factor 2'
names.append(name)
vars_names[name] = ['Power Factor', 'Active Power', 'Apparent Power']
variables[name] = ['PF', 'P', 'S']
formulas[name] = 'PF = P/S'
num_vars[name] = 3
equations[name] = power_factor_2
# 
# 
# 
def power_factor_three_fase(solv_vars, vars, dict_val):
    PF = vars[0]
    P = vars[1]
    U = vars[2]
    I = vars[3]

    eq = Eq(PF, P / (3**(1/2) * U * I))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Power Factor Three Fase'
names.append(name)
vars_names[name] = ['Power Factor', 'Power Applied', 'Voltage', 'Current']
variables[name] = ['PF', 'P', 'U', 'I']
formulas[name] = 'PF = P / (3**(1/2) * U * I)'
num_vars[name] = 4
equations[name] = power_factor_three_fase
# 
# 
# 
def capacitance(solv_vars, vars, dict_val):
    C = vars[0]
    Q = vars[1]
    U = vars[2]

    eq = Eq(C, Q / U)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Capacitance'
names.append(name)
vars_names[name] = ['Capacitance', 'Charge', 'Eletrical Potential']
variables[name] = ['C', 'Q', 'U']
formulas[name] = 'C = Q / U'
num_vars[name] = 3
equations[name] = capacitance
# 
# 
# 
def parallel_plate_capacitor(solv_vars, vars, dict_val):
    C = vars[0]
    epsilon_r = vars[1]
    epsilon_0 = vars[2]
    A = vars[3]
    D = vars[4]

    eq = Eq(C, epsilon_r*epsilon_0*A / d)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Parallel Plate Capacitor'
names.append(name)
vars_names[name] = ['Capacitance', 'Relative Permittivity', 'Absolute Permittivity', 'Area', 'Distance']
variables[name] = ['C', 'epsilon_r', 'epsilon_0', 'A', 'd']
formulas[name] = 'C = epsilon_r*epsilon_0*A / d'
num_vars[name] = 5
equations[name] = parallel_plate_capacitor
# 
# 
# 
def charge_of_capacitor(solv_vars, vars, dict_val):
    Q = vars[0]
    I = vars[1]
    t = vars[2]

    eq = Eq(Q, I*t)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Charge of Capacitor'
names.append(name)
vars_names[name] = ['Charge of Capacitor', 'Current', 'time']
variables[name] = ['Q', 'I', 't']
formulas[name] = 'Q = I*t'
num_vars[name] = 3
equations[name] = charge_of_capacitor
# 
# 
# 
def capacitor_dielectric_strength(solv_vars, vars, dict_val):
    E = vars[0]
    U = vars[1]
    d = vars[2]

    eq = Eq(E, U/d)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Capacitor Dielectric Strength'
names.append(name)
vars_names[name] = ['Electric Field Strength', 'Eletrical Potential', 'Distance']
variables[name] = ['E', 'U', 'd']
formulas[name] = 'E = U/d'
num_vars[name] = 3
equations[name] = capacitor_dielectric_strength
# 
# 
# 
def capacitor_electric_flux_density(solv_vars, vars, dict_val):
    D = vars[0]
    Q = vars[1]
    A = vars[2]

    eq = Eq(D, Q/A)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Capacitor Electric Flux Density'
names.append(name)
vars_names[name] = ['Electric Flux Density', 'Charge', 'Surface Area']
variables[name] = ['D', 'Q', 'A']
formulas[name] = 'D = Q/A'
num_vars[name] = 3
equations[name] = capacitor_electric_flux_density