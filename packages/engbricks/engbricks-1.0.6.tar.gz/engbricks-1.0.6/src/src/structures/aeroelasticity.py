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
#divergence
def aaa(solv_vars, vars, dict_val):
    theta = vars[0]
    rho = vars[1]
    V = vars[2]
    S = vars[3]
    c = vars[4]
    C_M_0 = vars[5]
    e = vars[6]
    C_L_0 = vars[7]
    d_C_L_d_alpha = vars[8]
    alpha = vars[9]
    K = vars[10]

    eq = Eq(theta, (1/2 * rho * V**2 * S * c * (C_M_0 + e * C_L_0 + e * d_C_L_d_alpha * alpha)) / (K - 1/2 * rho * V**2 * S * e * c * d_C_L_d_alpha))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'theta = (1/2 * rho * V**2 * S * c * (C_M_0 + e * C_L_0 + e * d_C_L_d_alpha * alpha)) / (K - 1/2 * rho * V**2 * S * e * c * d_C_L_d_alpha)'
num_vars['aaa'] = 11
equations['aaa'] = aaa
# 
# 
# 
def Divergence_Speed(solv_vars, vars, dict_val):
    V_divergence = vars[0]
    K = vars[1]
    rho = vars[2]
    S = vars[3]
    e = vars[4]
    c = vars[5]
    d_C_L_d_alpha = vars[6]

    eq = Eq(V_divergence, sqrt((2 * K) / (rho * S * e * c * d_C_L_d_alpha)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Divergence Speed')
vars_names['Divergence Speed'] = ['aaa', 'aaa', 'aaa']
variables['Divergence Speed'] = ['aaa', 'aaa', 'aaa']
formulas['Divergence Speed'] = 'V_divergence = sqrt((2 * K) / (rho * S * e * c * d_C_L_d_alpha))'
num_vars['Divergence Speed'] = 7
equations['Divergence Speed'] = Divergence_Speed
# 
# 
# 
#divergence finite wing
def aaa(solv_vars, vars, dict_val):
    theta = vars[0]
    C_m_0 = vars[1]
    e = vars[2]
    d_C_l_d_alpha = vars[3]
    alpha = vars[4]
    lambda_ = vars[5]
    b = vars[6]
    z = vars[7]

    eq = Eq(theta, ((C_m_0)*(e * d_C_l_d_alpha) + alpha) * ((cos(lambda_) * (b - z))/(cos(lambda_) * b) - 1))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'theta = ((C_m_0)*(e * d_C_l_d_alpha) + alpha) * ((cos(lambda) * (b - z))/(cos(lambda) * b) - 1)'
num_vars['aaa'] = 8
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    V_divergence = vars[0]
    G = vars[1]
    J = vars[2]
    rho = vars[3]
    e = vars[4]
    c = vars[5]
    b = vars[6]
    d_C_l_d_alpha = vars[7]

    eq = Eq(V_divergence, sqrt((math.pi**2 * G * J) / (2 * rho * e**2 * c * b**2 * d_C_l_d_alpha)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'V_divergence = sqrt((pi**2 * G * J) / (2 * rho * e**2 * c * b**2 * d_C_l_d_alpha))'
num_vars['aaa'] = 8
equations['aaa'] = aaa
# 
# 
# 
#Aileron effectiveness and reversal (two-dimensional case)
def aaa(solv_vars, vars, dict_val):
    theta = vars[0]
    rho = vars[1]
    V = vars[2]
    S = vars[3]
    c = vars[4]
    d_C_L_d_xi = vars[5]
    e = vars[6]
    d_C_M_0_d_xi = vars[7]
    xi = vars[8]
    K = vars[9]
    d_C_L_d_alpha = vars[10]


    eq = Eq(theta, (1/2 * rho * V**2 * S * c * (d_C_L_d_xi * e + d_C_M_0_d_xi) * xi) / (K - 1/2 * rho * V**2 * S * e * c * d_C_L_d_alpha))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'theta = (1/2 * rho * V**2 * S * c * (d_C_L_d_xi * e + d_C_M_0_d_xi) * xi) / (K - 1/2 * rho * V**2 * S * e * c * d_C_L_d_alpha)'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    V_r = vars[0]
    K = vars[1]
    d_C_L_d_xi = vars[2]
    rho = vars[3]
    S = vars[4]
    c = vars[5]
    d_C_M_0_d_xi = vars[6]
    d_C_L_d_alpha = vars[7]

    eq = Eq(V_r, sqrt((-K * d_C_L_d_xi) / (1/2 * rho * S * c * d_C_M_0_d_xi * d_C_L_d_alpha))
    )

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'V_r = sqrt((-K * d_C_L_d_xi) / (1/2 * rho * S * c * d_C_M_0_d_xi * d_C_L_d_alpha))'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    aileron_effectiviness = vars[0]
    rho = vars[1]
    S = vars[2]
    c = vars[3]
    d_C_M_0_d_xi = vars[4]
    d_C_L_d_alpha = vars[5]
    K = vars[6]
    d_C_L_d_xi = vars[7]
    V = vars[8]
    e = vars[9]

    eq = Eq(aileron_effectiviness, (1/2 * rho * S * c * d_C_M_0_d_xi * d_C_L_d_alpha + K + d_C_L_d_xi) / ((K - 1/2 * rho * V**2 * S * c * e * d_C_L_d_alpha) * d_C_L_d_xi))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('aaa')
vars_names['aaa'] = ['aaa', 'aaa', 'aaa']
variables['aaa'] = ['aaa', 'aaa', 'aaa']
formulas['aaa'] = 'aileron_effectiviness = (1/2 * rho * S * c * d_C_M_0_d_xi * d_C_L_d_alpha + K + d_C_L_d_xi) / ((K - 1/2 * rho * V**2 * S * c * e * d_C_L_d_alpha) * d_C_L_d_xi)'
num_vars['aaa'] = 3
equations['aaa'] = aaa
# 
# 
# 
# Aileron effectiveness and reversal (finite wing)
# 
# 
# 
# Introduction to ‘flutter’
# 
# 
# 