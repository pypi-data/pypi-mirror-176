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
def reynolds_number_1(solv_vars, vars, dict_val):
    Re = vars[0]
    V = vars[1]
    L = vars[2]
    rho = vars[3]
    mu = vars[4]

    eq = Eq(Re, (V * L * rho) / mu)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Reynolds Number 1'
names.append(name)
vars_names[name] = ['Reynolds Number', 'Velocity', 'Length', 'Density', 'Dynamic Viscosity']
variables[name] = ['Re', 'V', 'L', 'rho', 'mu']
formulas[name] = 'Re = (V * L * rho) / mu'
num_vars[name] = 5
equations[name] = reynolds_number_1
# 
# 
# 
def reynolds_number_2(solv_vars, vars, dict_val):
    Re = vars[0]
    V = vars[1]
    L = vars[2]
    nu = vars[3]

    eq = Eq(Re, (V * L) / nu)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Reynolds Number 2'
names.append(name)
vars_names[name] = ['Reynolds Number', 'Velocity', 'Length', 'Kinematics Viscosity']
variables[name] = ['Re', 'V', 'L', 'nu']
formulas[name] = 'Re = (V * L) / nu'
num_vars[name] = 4
equations[name] = reynolds_number_2
# 
# 
# 
def prandtl_number_1(solv_vars, vars, dict_val):
    Pr = vars[0]
    nu = vars[1]
    alpha = vars[2]

    eq = Eq(Pr, nu/alpha)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Prandtl Number 1'
names.append('Prandtl Number')
vars_names[name] = ['Prandtl Number', 'Kinematics Viscosity', 'Thermal Diffusivity']
variables[name] = ['Pr', 'nu', 'alpha']
formulas[name] = 'Pr = nu/alpha'
num_vars[name] = 3
equations[name] = prandtl_number_1
# 
# 
# 
def prandtl_number_2(solv_vars, vars, dict_val):
    Pr = vars[0]
    mu = vars[1]
    c_p = vars[2]
    k = vars[3]

    eq = Eq(Pr, (mu*c_p) / k)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Prandtl Number 2'
names.append(name)
vars_names[name] = ['Prandtl Number', 'Dynamic Viscosity', 'Specific Heat Capacity', 'Thermal Conductivity']
variables[name] = ['Pr', 'mu', 'c_p', 'k']
formulas[name] = 'Pr = (mu*c_p) / k'
num_vars[name] = 4
equations[name] = prandtl_number_2
# 
# 
# 
def grashof_number(solv_vars, vars, dict_val):
    Gr = vars[0]
    g = vars[1]
    beta = vars[2]
    T_s = vars[3]
    T_inf = vars[4]
    delta = vars[5]
    nu = vars[6]

    eq = Eq(Gr, (g * beta * (T_s - T_inf) * delta**3) / nu)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Grashof Number'
names.append(name)
vars_names[name] = ['Grashof Number', 'Grav Accel', 'Volume Expansion Coeff', 'Temp. Surface', 'Temp. Inf', 'Characteristic Length', 'Kinematics Viscosity']
variables[name] = ['Gr', 'g', 'beta', 'T_s', 'T_inf', 'delta', 'nu']
formulas[name] = 'Gr = (g * beta * (T_s - T_inf) * delta**3) / nu'
num_vars[name] = 7
equations[name] = grashof_number
# 
# 
# 
def rayleigh_number(solv_vars, vars, dict_val):
    Ra = vars[0]
    Gr = vars[1]
    Pr = vars[2]

    eq = Eq(Ra, Gr * Pr)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Rayleigh Number'
names.append(name)
vars_names[name] = ['Rayleigh Number', 'Grashof Number', 'Prandtl Number']
variables[name] = ['Ra', 'Gr', 'Pr']
formulas[name] = 'Ra = Gr * Pr'
num_vars[name] = 3
equations[name] = rayleigh_number
# 
# 
# 
def nusselt_number(solv_vars, vars, dict_val):
    Nu = vars[0]
    h = vars[1]
    L = vars[2]
    k = vars[3]

    eq = Eq(Nu, (h * L) / k)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Nusselt Number'
names.append(name)
vars_names[name] = ['Nusselt Number', 'Heat Transfer Coeff', 'Length', 'Thermal Conductivity']
variables[name] = ['Nu', 'h', 'L', 'k']
formulas[name] = 'Nu = (h * L) / k'
num_vars[name] = 4
equations[name] = nusselt_number
# 
# 
# 
# Isothermal Vertical Plate 10^4 < Ra < 10^9
def nusselt_number_1(solv_vars, vars, dict_val):
    Nu = vars[0]
    Ra = vars[1]

    eq = Eq(Nu, 0.59 * Ra**(1/4))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name ='Nusselt Number 1'
names.append(name)
vars_names[name] = ['Nusselt Number', 'Rayleigh Number']
variables[name] = ['Nu', 'Ra']
formulas[name] = 'Nu = 0.59 * Ra**(1/4)'
num_vars[name] = 2
equations[name] = nusselt_number_1
# 
# 
# 
# Isothermal Vertical Plate 10^9 < Ra < 10^13
def nusselt_number_2(solv_vars, vars, dict_val):
    Nu = vars[0]
    Ra = vars[1]

    eq = Eq(Nu, 0.1 * Ra**(1/3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Nusselt Number 2'
names.append(name)
vars_names[name] = ['Nusselt Number', 'Rayleigh Number']
variables[name] = ['Nu', 'Ra']
formulas[name] = 'Nu = 0.1 * Ra**(1/3)'
num_vars[name] = 2
equations[name] = nusselt_number_2
# 
# 
# 
# Isothermal Horizontal Plate Upper surface 10^4 < Ra < 10^7
def nusselt_number_3(solv_vars, vars, dict_val):
    Nu = vars[0]
    Ra = vars[1]

    eq = Eq(Nu, 0.54 * Ra**(1/4))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Nusselt Number 3'
names.append(name)
vars_names[name] = ['Nusselt Number', 'Rayleigh Number']
variables[name] = ['Nu', 'Ra']
formulas[name] = 'Nu = 0.54 * Ra**(1/4)'
num_vars[name] = 2
equations[name] = nusselt_number_3
# 
# 
# 
# Isothermal Horizontal Plate Upper surface 10^7 < Ra < 10^11
def nusselt_number_4(solv_vars, vars, dict_val):
    Nu = vars[0]
    Ra = vars[1]

    eq = Eq(Nu, 0.15 * Ra**(1/3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Nusselt Number 4'
names.append(name)
vars_names[name] = ['Nusselt Number', 'Rayleigh Number']
variables[name] = ['Nu', 'Ra']
formulas[name] = 'Nu = 0.15 * Ra**(1/3)'
num_vars[name] = 2
equations[name] = nusselt_number_4
# 
# 
# 
# Isothermal Horizontal Plate Lower surface 10^5 < Ra < 10^11
def nusselt_number_5(solv_vars, vars, dict_val):
    Nu = vars[0]
    Ra = vars[1]

    eq = Eq(Nu, 0.27 * Ra**(1/4))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Nusselt Number 5'
names.append(name)
vars_names[name] = ['Nusselt Number', 'Rayleigh Number']
variables[name] = ['Nu', 'Ra']
formulas[name] = 'Nu = 0.27 * Ra**(1/4)'
num_vars[name] = 2
equations[name] = nusselt_number_5
# 
# 
# 
def biot_number(solv_vars, vars, dict_val):
    Bi = vars[0]
    h = vars[1]
    L_c = vars[2]
    k = vars[3]

    eq = Eq(Bi, (h * L_c) / k)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Biot Number'
names.append(name)
vars_names[name] = ['Biot Number', 'Heat Transfer Coeff', 'Characteristic Length', 'Thermal conductivity']
variables[name] = ['Bi', 'h', 'L_c', 'k']
formulas[name] = 'Bi = (h * L_c) / k'
num_vars[name] = 4
equations[name] = biot_number
# 
# 
# 
def mach_number(solv_vars, vars, dict_val):
    M = vars[0]
    V = vars[1]
    a = vars[2]

    eq = Eq(M, V/a)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Mach Number'
names.append(name)
vars_names[name] = ['Mach', 'Velocity', 'Speed of Sound']
variables[name] = ['M', 'V', 'a']
formulas[name] = 'M = V/a'
num_vars[name] = len(variables[name])
equations[name] = mach_number
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