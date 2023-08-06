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



#Symbols
M, \
t_c, \
A_W, \
A_H, \
uc_lambda_n, \
uc_lambda_m, \
uc_lambda_LE_W, \
uc_lambda_c_2_W, \
uc_lambda_c_4_W, \
uc_lambda_LE_H, \
uc_lambda_c_2_H, \
uc_lambda_c_4_H, \
uc_lambda_LE_V, \
uc_lambda_c_2_V, \
uc_lambda_c_4_V, \
b_W, \
b_H, \
b_V, \
S_W, \
S_H, \
S_V, \
lc_lambda_W, \
lc_lambda_H, \
lc_lambda_V, \
c_T_W, \
c_T_H, \
c_T_V, \
c_R_W, \
c_R_H, \
c_R_V, \
phi_TE, \
C_D, \
C_D_0, \
C_L, \
e, \
C_D_alpha, \
C_L_alpha, \
C_L_alpha_W, \
C_L_alpha_W_M0, \
C_L_alpha_H, \
C_L_alpha_WB, \
W, \
q, \
rho, \
V, \
eta_H, \
epsilon, \
K_WB, \
d, \
uc_beta_1, \
uc_beta_2, \
lc_kappa, \
K, \
K_A, \
K_lambda, \
K_H, \
h_H, \
l_H, \
C_m_alpha, \
d_C_m_d_C_L, \
X_ac_mean, \
c_mean, \
X_cg_mean, \
X_ac_W, \
X_ac_W_mean, \
X_ac_H, \
X_ac_H_mean, \
X_ac_B, \
X_ac_B_mean, \
C_D_u, \
C_L_u, \
C_m_u, \
C_D_q, \
C_L_q, \
C_L_q_W, \
C_L_q_W_M0, \
C_L_q_H, \
C_m_q, \
C_m_q_W, \
C_m_q_W_M0, \
C_m_q_H, \
V_H, \
X_H, \
V_V, \
X_V, \
C_D_alpha_dot, \
C_L_alpha_dot, \
C_m_alpha_dot, \
C_y_beta, \
lc_beta, \
uc_gamma, \
C_l_beta, \
C_n_beta, \
C_y_p, \
C_l_p, \
C_n_p, \
C_y_r, \
C_l_r, \
C_n_r, \
C_L_delta_F, \
C_m_delta_F, \
C_L_delta_E, \
C_m_delta_E, \
C_L_i_H, \
C_m_i_H, \
C_y_delta_A, \
C_l_delta_A, \
C_n_delta_A, \
C_y_delta_R, \
C_l_delta_R, \
C_n_delta_R, \
d_C_D_0_d_alpha, \
d_epsilon_d_alpha_M0, \
d_epsilon_d_alpha, \
K1, \
K2, \
d_C_D_d_M, \
d_X_ac_W_mean_d_M \
= \
symbols( \
'M, \
t_c, \
A_W, \
A_H, \
uc_lambda_n, \
uc_lambda_m, \
uc_lambda_LE_W, \
uc_lambda_c_2_W, \
uc_lambda_c_4_W, \
uc_lambda_LE_H, \
uc_lambda_c_2_H, \
uc_lambda_c_4_H, \
uc_lambda_LE_V, \
uc_lambda_c_2_V, \
uc_lambda_c_4_V, \
b_W, \
b_H, \
b_V, \
S_W, \
S_H, \
S_V, \
lc_lambda_W, \
lc_lambda_H, \
lc_lambda_V, \
c_T_W, \
c_T_H, \
c_T_V, \
c_R_W, \
c_R_H, \
c_R_V, \
phi_TE, \
C_D, \
C_D_0, \
C_L, \
e, \
C_D_alpha, \
C_L_alpha, \
C_L_alpha_W, \
C_L_alpha_W_M0, \
C_L_alpha_H, \
C_L_alpha_WB, \
W, \
q, \
rho, \
V, \
eta_H, \
epsilon, \
K_WB, \
d, \
uc_beta_1, \
uc_beta_2, \
lc_kappa, \
K, \
K_A, \
K_lambda, \
K_H, \
h_H, \
l_H, \
C_m_alpha, \
d_C_m_d_C_L, \
X_ac_mean, \
c_mean, \
X_cg_mean, \
X_ac_W, \
X_ac_W_mean, \
X_ac_H, \
X_ac_H_mean, \
X_ac_B, \
X_ac_B_mean, \
C_D_u, \
C_L_u, \
C_m_u, \
C_D_q, \
C_L_q, \
C_L_q_W, \
C_L_q_W_M0, \
C_L_q_H, \
C_m_q, \
C_m_q_W, \
C_m_q_W_M0, \
C_m_q_H, \
V_H, \
X_H, \
V_V, \
X_V, \
C_D_alpha_dot, \
C_L_alpha_dot, \
C_m_alpha_dot, \
C_y_beta, \
lc_beta, \
uc_gamma, \
C_l_beta, \
C_n_beta, \
C_y_p, \
C_l_p, \
C_n_p, \
C_y_r, \
C_l_r, \
C_n_r, \
C_L_delta_F, \
C_m_delta_F, \
C_L_delta_E, \
C_m_delta_E, \
C_L_i_H, \
C_m_i_H, \
C_y_delta_A, \
C_l_delta_A, \
C_n_delta_A, \
C_y_delta_R, \
C_l_delta_R, \
C_n_delta_R, \
d_C_D_0_d_alpha, \
d_epsilon_d_alpha_M0, \
d_epsilon_d_alpha, \
K1, \
K2, \
d_C_D_d_M, \
d_X_ac_W_mean_d_M \
')

W = 10000
rho = 1.225

K1 = 1.3

K2 = 1.3

c_mean = 5
X_ac_W = 2
X_ac_H = 10

X_ac_W_mean = X_ac_W / c_mean
X_ac_H_mean = X_ac_H / c_mean


# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(aaa, aaa/aaa)

#     results = solve(eq, solv_vars[0], dict = dict_val)

#    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def uc_lambda_func(solv_vars, vars, dict_val):
    uc_lambda_n = vars[0]
    uc_lambda_m = vars[1]
    n = vars[2]
    m = vars[3]
    A = vars[4]
    lc_lambda = vars[5]

    eq = Eq(uc_lambda_n, uc_lambda_m - 4/A * (n-m) * ((1-lc_lambda)/(1+lc_lambda)))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def uc_beta_2_func(solv_vars, vars, dict_val):
    uc_beta_2 = vars[0]
    M = vars[1]
    uc_lambda_c_4_W = vars[2]

    eq = Eq(uc_beta_2, sqrt(1 - M**2 * (cos(uc_lambda_c_4_W))**2))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def K_WB_func(solv_vars, vars, dict_val):
    K_WB = vars[0]
    d = vars[1]
    b_W = vars[2]

    eq = Eq(K_WB, 1 - 0.25 * (d/b_W)**2 + 0.025 * (d/b_W))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def lc_beta_func(solv_vars, vars, dict_val):
    lc_beta = vars[0]
    M = vars[1]

    eq = Eq(lc_beta, sqrt(1 - M**2))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def K_A_func(solv_vars, vars, dict_val):
    K_A = vars[0]
    A = vars[1]

    eq = Eq(K_A, 1/A - 1/(1 + A**1.7))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def K_lambda_func(solv_vars, vars, dict_val):
    K_lambda = vars[0]
    lc_lambda = vars[1]

    eq = Eq(K_lambda, (10 - 3 * lc_lambda)/7)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def K_H_func(solv_vars, vars, dict_val):
    K_H = vars[0]
    h_H = vars[1]
    l_H = vars[2]
    b = vars[3]

    eq = Eq(K_H, (1 - h_H/b) / ((2 * l_H/b)**1/3))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#angle of attack derivatives
#C_L_alpha
def C_L_alpha_W_func(solv_vars, vars, dict_val):
    C_L_alpha_W = vars[0]
    A_W = vars[1]
    lc_beta = vars[2]
    lc_kappa = vars[3]
    uc_lambda_c_2_W = vars[4]

    expr_1 = A_W**2 * lc_beta**2 / lc_kappa * (1 + (tan(math.radians(uc_lambda_c_2_W)))**2 / lc_beta**2) + 4

    eq = Eq(C_L_alpha_W, 2 * pi * A_W / (2 + sqrt(expr_1)))

    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_L_alpha_WB_func(solv_vars, vars, dict_val):
    C_L_alpha_WB = vars[0]
    K_WB = vars[1]
    C_L_alpha_W = vars[2]

    eq = Eq(C_L_alpha_WB, K_WB * C_L_alpha_W)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_L_alpha_H_func(solv_vars, vars, dict_val):
    C_L_alpha_H = vars[0]
    A_H = vars[1]
    lc_beta = vars[2]
    lc_kappa = vars[3]
    uc_lambda_c_2_W = vars[4]

    expr_1 = A_H**2 * lc_beta**2 / lc_kappa * (1 + (tan(math.radians(uc_lambda_c_2_W)))**2 / lc_beta**2) + 4

    eq = Eq(C_L_alpha_W, 2 * pi * A_H / (2 + sqrt(expr_1)))

    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def d_epsilon_d_alpha_M0_func(solv_vars, vars, dict_val):
    d_epsilon_d_alpha_M0 = vars[0]
    K_A = vars[1]
    K_lambda = vars[2]
    K_H = vars[3]
    uc_lambda_c_4 = vars[4]

    eq = Eq(d_epsilon_d_alpha_M0, 4.44 * (K_A * K_lambda * K_H * sqrt(cos(math.radians(uc_lambda_c_4))))**1.19)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def d_epsilon_d_alpha_func(solv_vars, vars, dict_val):
    d_epsilon_d_alpha = vars[0]
    d_epsilon_d_alpha_M0 = vars[1]
    C_L_alpha_W = vars[2]
    C_L_alpha_W_M0 = vars[3]

    eq = Eq(d_epsilon_d_alpha, d_epsilon_d_alpha_M0 * (C_L_alpha_W / C_L_alpha_W_M0))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_L_alpha_func(solv_vars, vars, dict_val):
    C_L_alpha = vars[0]
    C_L_alpha_WB = vars[1]
    C_L_alpha_H = vars[2]
    eta_H = vars[3]
    S_H = vars[4]
    S = vars[5]
    d_epsilon_d_alpha = vars[6]

    eq = Eq(C_L_alpha, C_L_alpha_WB + C_L_alpha_H * (eta_H * S_H/S * (1 - d_epsilon_d_alpha)))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#eta_H -> dynamic pressure ratio at the horizontal tail can be assumed as: 0.9 <eta_H <1.0





#C_D_alpha
def C_D_alpha_func(solv_vars, vars, dict_val):
    C_D_alpha = vars[0]
    d_C_D_0_d_alpha = vars[1]
    C_L = vars[2]
    C_L_alpha = vars[3]
    A_W = vars[4]
    e = vars[5]

    eq = Eq(C_D_alpha, d_C_D_0_d_alpha + (2.0 * C_L * C_L_alpha)/(2.0 * pi * A_W * e))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_m_alpha


X_ac_B_mean = 1.2
X_cg_mean = 3

def X_ac_func(solv_vars, vars, dict_val):
    X_ac_mean = vars[0]
    X_ac_W_mean = vars[1]
    X_ac_B_mean = vars[2]
    C_L_alpha_H = vars[3]
    C_L_alpha_WB = vars[4]
    eta_H = vars[5]
    S_H = vars[6]
    S_W = vars[7]
    X_ac_H_mean = vars[8]
    d_epsilon_d_alpha = vars[9]

    expr_1 = X_ac_W_mean + X_ac_B_mean + C_L_alpha_H/C_L_alpha_WB * eta_H * S_H/S_W * X_ac_H_mean * (1 - d_epsilon_d_alpha)

    expr_2 = 1 + C_L_alpha_H/C_L_alpha_WB * eta_H * S_H/S_W * (1 - d_epsilon_d_alpha)

    eq = Eq(X_ac_mean, expr_1 / expr_2)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def d_C_m_d_C_L_func(solv_vars, vars, dict_val):
    d_C_m_d_C_L = vars[0]
    X_cg_mean = vars[1]
    X_ac_mean = vars[2]

    eq = Eq(d_C_m_d_C_L, X_cg_mean - X_ac_mean)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_m_alpha_func(solv_vars, vars, dict_val):
    C_m_alpha = vars[0]
    d_C_m_d_C_L = vars[1]
    C_L_alpha = vars[2]

    eq = Eq(C_m_alpha, d_C_m_d_C_L * C_L_alpha)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#speed derivatives
#C_D_u

def d_C_D_d_M_func(solv_vars, vars, dict_val):
    d_C_D_d_M = vars[0]
    A = vars[1]
    e = vars[2]
    W = vars[3]
    rho = vars[4]
    S = vars[5]
    a = vars[6]
    M = vars[7]

    eq = Eq(d_C_D_d_M, 1 / (pi * A * e) * W**2 / (0.5**2 * rho**2 * S**2 * a**4) * (-4) * M**(-5))

    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_D_u_func(solv_vars, vars, dict_val):
    C_D_u = vars[0]
    M = vars[1]
    C_L = vars[2]

    eq = Eq(C_D_u, M * C_L)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_L_u
def C_L_u_func(solv_vars, vars, dict_val):
    C_L_u = vars[0]
    M = vars[1]
    C_L = vars[2]

    eq = Eq(C_L_u, M**2/(1 - M**2) * C_L)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_m_u
# def d_X_ac_W_mean_d_M_func(solv_vars, vars, dict_val):
#     d_X_ac_W_mean_d_M = vars[0]
#     M = vars[1]
#     C_L = vars[2]

#     eq = Eq(d_X_ac_W_mean_d_M - (M**2/(1 - M**2) * C_L)
    
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
d_X_ac_W_mean_d_M = 0.2

def C_m_u_func(solv_vars, vars, dict_val):
    C_m_u = vars[0]
    C_L = vars[1]
    d_X_ac_W_mean_d_M = vars[2]

    eq = Eq(C_m_u, -C_L * d_X_ac_W_mean_d_M)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#pitch rate derivatives
#C_D_q
#in subsonic mach range this derivative is usually negligible
def C_D_q_func(solv_vars, vars, dict_val):
    C_D_q = vars[0]

    eq = Eq(C_D_q, 0.0)
    
    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_L_q
def C_L_q_W_M0_func(solv_vars, vars, dict_val):
    C_L_q_W_M0 = vars[0]
    X_W = vars[1]
    c_mean = vars[2]
    C_L_alpha_W_M0 = vars[3]

    eq = Eq(C_L_q_W_M0, (1/2 + 2 * X_W/c_mean) * C_L_alpha_W_M0)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_L_q_W_func(solv_vars, vars, dict_val):
    C_L_q_W = vars[0]
    A_W = vars[1]
    uc_beta_2 = vars[2]
    uc_lambda_c_4_W = vars[3]
    C_L_q_W_M0 = vars[4]

    eq = Eq(C_L_q_W, (A_W + 2 * cos(uc_lambda_c_4_W))/(A_W * uc_beta_2 + 2 * cos(uc_lambda_c_4_W)) * C_L_q_W_M0)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def tail_volume_coef_func(solv_vars, vars, dict_val):
    tail_volume_coef = vars[0]
    X = vars[1]
    c_mean = vars[2]
    S = vars[3]
    S_tail = vars[4]

    eq = Eq(tail_volume_coef, X / c_mean * S_tail / S)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_L_q_H_func(solv_vars, vars, dict_val):
    C_L_q_H = vars[0]
    C_L_alpha_H = vars[1]
    eta_H = vars[2]
    V_H = vars[3]

    eq = Eq(C_L_q_H, 2 * C_L_alpha_H * eta_H * V_H)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_L_q_func(solv_vars, vars, dict_val):
    C_L_q = vars[0]
    C_L_q_W = vars[1]
    C_L_q_H = vars[2]

    eq = Eq(C_L_q, C_L_q_W + C_L_q_H)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_m_q
def K_func(solv_vars, vars, dict_val):
    K = vars[0]
    A = vars[1]

    eq = Eq(K, tanh(A-8) * 0.1 + 0.8)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_m_q_W_M0_func(solv_vars, vars, dict_val):
    C_m_q_W_M0 = vars[0]
    K = vars[1]
    C_l_alpha_W = vars[2]
    uc_lambda_c_4_W = vars[3]
    A_W = vars[4]
    X_W = vars[5]
    c_mean = vars[6]

    expr_1 = (A_W * (2 * (X_W/c_mean)**2 + 1/2 * X_W/c_mean)) / (A_W + 2 * cos(uc_lambda_c_4_W))

    expr_2 = 1/24 * (A_W**3 * (tan(uc_lambda_c_4_W))**2) / (A_W + 6 * cos(uc_lambda_c_4_W))

    eq = Eq(C_m_q_W_M0, -K * C_l_alpha_W * cos(uc_lambda_c_4_W) * (expr_1 + expr_2 + 1/8))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_m_q_W_func(solv_vars, vars, dict_val):
    C_m_q_W = vars[0]
    C_m_q_W_M0 = vars[1]
    A_W = vars[2]
    uc_lambda_c_4_W = vars[3]
    uc_beta_2 = vars[4]

    eq = Eq(C_m_q_W, C_m_q_W_M0 * (((A_W**3 * (tan(uc_lambda_c_4_W))**2)/(A_W * uc_beta_2 + 6 * cos(uc_lambda_c_4_W)) + 3/uc_beta_2) / ((A_W**3 * (tan(uc_lambda_c_4_W))**2) / (A_W + 6 * cos(uc_lambda_c_4_W)) + 3)))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_m_q_H_func(solv_vars, vars, dict_val):
    C_m_q_H = vars[0]
    C_L_alpha_H = vars[1]
    eta_H = vars[2]
    V_H = vars[3]
    X_H = vars[4]
    c_mean = vars[5]

    eq = Eq(C_m_q_H, -2 * C_L_alpha_H * eta_H * V_H * X_H/c_mean)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
def C_m_q_func(solv_vars, vars, dict_val):
    C_m_q = vars[0]
    C_m_q_W = vars[1]
    C_m_q_H = vars[2]

    eq = Eq(C_m_q, C_m_q_W + C_m_q_H)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#angle of attack rate derivatives
#C_D_alpha_dot
#in subsonic mach range this derivative is usually negligible
def C_D_alpha_dot_func(solv_vars, vars, dict_val):
    C_D_alpha_dot = vars[0]

    eq = Eq(C_D_alpha_dot, 0.0)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_L_alpha_dot
#C_m_alpha_dot

#angle of sideslip derivatives
#C_y_beta
#C_l_beta
#C_n_beta

#roll rate derivatives
#C_y_p
#C_l_p
#C_n_p

#yaw rate derivatives
#C_y_r
#C_l_r
#C_n_r

#longitudinal control derivatives
#C_L_delta_F
#C_m_delta_F
#C_L_i_H
def C_L_i_H_func(solv_vars, vars, dict_val):
    C_L_i_H = vars[0]
    C_L_alpha_H = vars[1]
    S_H = vars[2]
    S_W = vars[3]

    eq = Eq(C_L_i_H, C_L_alpha_H * S_H / S_W)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_m_i_H
def C_m_i_H_func(solv_vars, vars, dict_val):
    C_m_i_H = vars[0]
    C_L_alpha_H = vars[1]
    V_H = vars[2]

    eq = Eq(C_m_i_H, -C_L_alpha_H * V_H)
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_L_delta_E
#C_m_delta_E

#lateral control derivatives
#C_y_delta_A
#C_l_delta_A
#C_n_delta_A

#directional control derivatives
#C_y_delta_R
C_y_delta_R = 0.2

#C_l_delta_R
def C_l_delta_R_func(solv_vars, vars, dict_val):
    C_l_delta_R = vars[0]
    C_y_delta_R = vars[1]
    Z_V = vars[2]
    l_V = vars[3]
    b = vars[4]
    alpha = vars[5]

    eq = Eq(C_l_delta_R, C_y_delta_R * ((Z_V * cos(alpha) - l_V * sin(alpha)) / b))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 
#C_n_delta_R
def C_n_delta_R_func(solv_vars, vars, dict_val):
    C_n_delta_R = vars[0]
    C_y_delta_R = vars[1]
    Z_V = vars[2]
    l_V = vars[3]
    b = vars[4]
    alpha = vars[5]

    eq = Eq(C_n_delta_R, -C_y_delta_R * ((l_V * cos(alpha) + Z_V * sin(alpha)) / b))
    
    results = solve(eq, solv_vars[0], dict = dict_val)
    
    return results

name = 'aaa'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['aaa', 'aaa', 'aaa']
formulas[name] = 'aaa = aaa/aaa'
num_vars[name] = len(variables[name])
equations[name] = aaa
# 
# 
# 