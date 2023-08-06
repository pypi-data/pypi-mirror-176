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
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(sigma_z, ((M_y * I_xx - M_x * I_xy)/(I_xx * I_yy - I_xy**2) * x) - ((M_x * I_yy - M_y * I_xy)/(I_xx * I_yy - I_xy**2 ) * y))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'aaa = aaa/aaa'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(tan(alpha), (M_y * I_xx - M_x * I_xy)/(M_x * I_yy - M_y * I_xy))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'aaa = aaa/aaa'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(q_s, q_s_ant + ((S_x * I_xx - S_y * I_xy)/(I_xx * I_yy - I_xy**2) * integrate(t * x, (s, 0, s_n))) + ((S_y * I_yy - S_x * I_xy)/(I_xx * I_yy - I_xy**2) * integrate(t * y, (s, 0, s_n))))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'aaa = aaa/aaa'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 