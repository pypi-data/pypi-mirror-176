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
def aaa(solv_vars, vars, dict_val):
    P = vars[0]
    d = vars[1]
    tau_1 = vars[2]
    b = vars = [3]

    eq = Eq(P, (math.pi * d**2 * tau_1)/(4 * b))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['P', 'd', 'tau_1', 'b']
formulas['aaa'] = 'P = (pi * d**2 * tau_1)/(4 * b)'
num_vars['aaa'] = 4
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    P_b = vars[0]
    P = vars[1]
    b = vars[2]
    t = vars[3]
    d = vars[4]

    eq = Eq(P_b, (P * b)/(t * d))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['P_b', 'P', 'b', 't', 'd']
formulas['aaa'] = 'P_b = (P * b)/(t * d)'
num_vars['aaa'] = 5
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    P = vars[0]
    sigma_ult = vars[1]
    t = vars[2]
    b = vars[3]
    d = vars[4]

    eq = Eq(P, (sigma_ult * t * (b - d))/(b))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['P', 'sigma_ult', 't', 'b', 'd']
formulas['aaa'] = 'P = (sigma_ult * t * (b - d))/(b)'
num_vars['aaa'] = 5
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    P = vars[0]
    a = vars[1]
    t = vars[2]
    tau_2 = vars[3]
    b = vars[4]

    eq = Eq(P, (2 * a * t* tau_2)/(b))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['P', 'a', 't', 'tau_2', 'b']
formulas['aaa'] = 'P = (2 * a * t* tau_2)/(b)'
num_vars['aaa'] = 5
equations['aaa'] = aaa
# 
# 
# 