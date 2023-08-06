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
#normal stress
def aaa(solv_vars, vars, dict_val):
    sigma_n = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]
    theta = vars[3]
    tau_xy = vars[4]

    eq = Eq(sigma_n, (sigma_x * (cos(theta))**2 + sigma_y * (sin(theta))**2 + tau_xy * sin(2*theta)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'sigma_n - (sigma_x * (cos(theta))**2 + sigma_y * (sin(theta))**2 + tau_xy * sin(2*theta))'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    sigma_1 = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]
    tau_xy = vars[3]

    eq = Eq(sigma_1, ((sigma_x + sigma_y)/2 + 1/2 * sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'sigma_1 - ((sigma_x + sigma_y)/2 + 1/2 * sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2))'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    sigma_2 = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]
    tau_xy = vars[3]

    eq = Eq(sigma_2, ((sigma_x + sigma_y)/2 - 1/2 * sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'sigma_2 - ((sigma_x + sigma_y)/2 - 1/2 * sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2))'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
#shear stress
def aaa(solv_vars, vars, dict_val):
    tau = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]
    tau_xy = vars[3]
    theta = vars[4]


    eq = Eq(tau, ((sigma_x - sigma_y)/2 * (sin(2*theta)) - tau_xy * cos(2*theta)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'tau - ((sigma_x - sigma_y)/2 * (sin(2*theta)) - tau_xy * cos(2*theta))'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    tau_max = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]
    tau_xy = vars[3]

    eq = Eq(tau_max, 1/2 * sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'tau_max - 1/2 * sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2)'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def radius(solv_vars, vars, dict_val):
    aaa = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]
    tau_xy = vars[3]

    eq = Eq(radius, 1/2 * math.sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'radius = 1/2 * math.sqrt((sigma_x-sigma_y)**2 + 4*tau_xy**2)'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    center = vars[0]
    sigma_x = vars[1]
    sigma_y = vars[2]

    eq = Eq(center, (sigma_x-sigma_y)/2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'center = (sigma_x-sigma_y)/2'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 