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
def fiber_volume_fraction(solv_vars, vars, dict_val):
    Vf = vars[0]
    vf = vars[1]
    vc = vars[2]

    eq = Eq(Vf, vf/vc)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Fiber Volume Fraction'
names.append(name)
vars_names[name] = ['Fiber Volume Fraction', 'Fiber Volume', 'Composite Volume']
variables[name] = ['Vf', 'vf', 'vc']
formulas[name] = 'Vf = vf/vc'
num_vars[name] = 3
equations[name] = fiber_volume_fraction
# 
# 
# 
def matrix_volume_fraction(solv_vars, vars, dict_val):
    Vm = vars[0]
    vm = vars[1]
    vc = vars[2]

    eq = Eq(Vm, vm/vc)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Matrix Volume Fraction'
names.append(name)
vars_names[name] = ['Matrix Volume Fraction', 'Matrix Volume', 'Composite Volume']
variables[name] = ['Vm', 'vm', 'vc']
formulas[name] = 'Vm = vm/vc'
num_vars[name] = 3
equations[name] = matrix_volume_fraction
# 
# 
# 
def Fiber_Mass_Fraction(solv_vars, vars, dict_val):
    Wf = vars[0]
    wf = vars[1]
    wc = vars[2]

    eq = Eq(Wf, wf/wc)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Fiber Mass Fraction')
vars_names['Fiber Mass Fraction'] = ['Fiber Mass Fraction', 'Fiber Mass', 'Composite Mass']
variables['Fiber Mass Fraction'] = ['Wf', 'wf', 'wc']
formulas['Fiber Mass Fraction'] = 'Wf = wf/wc'
num_vars['Fiber Mass Fraction'] = 3
equations['Fiber Mass Fraction'] = Fiber_Mass_Fraction
# 
# 
# 
def Matrix_Mass_Fraction(solv_vars, vars, dict_val):
    Wm = vars[0]
    wm = vars[1]
    wc = vars[2]

    eq = Eq(Wm, wm/wc)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Matrix Mass Fraction')
vars_names['Matrix Mass Fraction'] = ['Matrix Mass Fraction', 'Matrix Mass', 'Composite Mass']
variables['Matrix Mass Fraction'] = ['Wm', 'wm', 'wc']
formulas['Matrix Mass Fraction'] = 'Wm = wm/wc'
num_vars['Matrix Mass Fraction'] = 3
equations['Matrix Mass Fraction'] = Matrix_Mass_Fraction
# 
# 
# 
def Mixture_Law(solv_vars, vars, dict_val):
    E_1 = vars[0]
    E_f = vars[1]
    E_m = vars[2]
    V_f = vars[3]
    V_m = vars[4]

    eq = Eq(E_1, (V_f * E_f + V_m * E_m))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Mixture Law')
vars_names['Mixture Law'] = ['Composite Elastic Module', 'Fiber Elastic Module', 'Matrix Elastic Module', 'Fiber Volume Fraction', 'Matrix Volume Fraction']
variables['Mixture Law'] = ['E_1', 'E_f', 'E_m', 'V_f', 'V_m']
formulas['Mixture Law'] = 'E_1 = (V_f * E_f + V_m * E_m)'
num_vars['Mixture Law'] = 5
equations['Mixture Law'] = Mixture_Law
# 
# 
# 
#non interactive failur criteria
def Max_Stress_Traction_X(solv_vars, vars, dict_val):
    max_stress_traction_X = vars[0]
    sigma_1 = vars[1]
    sigma_X_t = vars[2]

    eq = Eq(max_stress_traction_X, sigma_1 / sigma_X_t)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Stress Traction X')
vars_names['Max Stress Traction X'] = ['Max Stress Traction X', 'Long. Tension', 'Long. Failure Tension']
variables['Max Stress Traction X'] = ['max_stress_traction_X', 'sigma_1', 'sigma_X_t']
formulas['Max Stress Traction X'] = 'max_stress_traction_X = sigma_1 / sigma_X_t'
num_vars['Max Stress Traction X'] = 3
equations['Max Stress Traction X'] = Max_Stress_Traction_X
# 
# 
# 
def Max_Stress_Traction_Y(solv_vars, vars, dict_val):
    max_stress_traction_Y = vars[0]
    sigma_2 = vars[1]
    sigma_Y_t = vars[2]

    eq = Eq(max_stress_traction_Y, sigma_2 / sigma_Y_t)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Stress Traction Y')
vars_names['Max Stress Traction Y'] = ['Max Stress Traction Y', 'Transverse Tension', 'Transverse Failure Tension']
variables['Max Stress Traction Y'] = ['max_stress_traction_Y', 'sigma_2', 'sigma_Y_t']
formulas['Max Stress Traction Y'] = 'max_stress_traction_Y = sigma_2 / sigma_Y_t'
num_vars['Max Stress Traction Y'] = 3
equations['Max Stress Traction Y'] = Max_Stress_Traction_Y
# 
# 
# 
def Max_Stress_Compression_X(solv_vars, vars, dict_val):
    value = vars[0]
    sigma_1 = vars[1]
    sigma_X_c = vars[2]

    eq = Eq(value, abs(sigma_1) / abs(sigma_X_c))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Stress Compression X')
vars_names['Max Stress Compression X'] = ['Max Stress Compression X', 'aaa', 'aaa']
variables['Max Stress Compression X'] = ['h', 'sigma_1', 'sigma_X_c']
formulas['Max Stress Compression X'] = 'value = abs(sigma_1) / abs(sigma_X_c)'
num_vars['Max Stress Compression X'] = 3
equations['Max Stress Compression X'] = Max_Stress_Compression_X
# 
# 
# 
def Max_Stress_Compression_Y(solv_vars, vars, dict_val):
    value = vars[0]
    sigma_2 = vars[1]
    sigma_Y_c = vars[2]

    eq = Eq(value, abs(sigma_2) / abs(sigma_Y_c))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Stress Compression Y')
vars_names['Max Stress Compression Y'] = ['Max Stress Compression Y', 'lambda_1', 'Temp at 0m', 'aaa']
variables['Max Stress Compression Y'] = ['h', 'sigma_2', 'sigma_Y_c']
formulas['Max Stress Compression Y'] = 'value = abs(sigma_2) / abs(sigma_Y_c)'
num_vars['Max Stress Compression Y'] = 3
equations['Max Stress Compression Y'] = Max_Stress_Compression_Y
# 
# 
# 
def Max_Stress_Shear(solv_vars, vars, dict_val):
    value = vars[0]
    sigma_12 = vars[1]
    sigma_S = vars[2]

    eq = Eq(value, abs(sigma_12) / sigma_S)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Stress Shear')
vars_names['Max Stress Shear'] = ['Max Stress Shear', 'aaa', 'aaa']
variables['Max Stress Shear'] = ['aaa', 'sigma_12', 'sigma_S']
formulas['Max Stress Shear'] = 'value = abs(sigma_12) / sigma_S'
num_vars['Max Stress Shear'] = 3
equations['Max Stress Shear'] = Max_Stress_Shear
# 
# 
# 
def Max_Strain_Traction_X(solv_vars, vars, dict_val):
    value = vars[0]
    epsilon_1 = vars[1]
    epsilon_X_t = vars[2]

    eq = Eq(value, epsilon_1 / epsilon_X_t)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Strain Traction X')
vars_names['Max Strain Traction X'] = ['Max Strain Traction X', 'aaa', 'aaa']
variables['Max Strain Traction X'] = ['aaa', 'epsilon_1', 'epsilon_X_t']
formulas['Max Strain Traction X'] = 'value = epsilon_1 / epsilon_X_t'
num_vars['Max Strain Traction X'] = 3
equations['Max Strain Traction X'] = Max_Strain_Traction_X
# 
# 
# 
def Max_Strain_Traction_Y(solv_vars, vars, dict_val):
    value = vars[0]
    epsilon_2 = vars[1]
    epsilon_Y_t = vars[2]

    eq = Eq(value, epsilon_2 / epsilon_Y_t)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Strain Traction Y')
vars_names['Max Strain Traction Y'] = ['Max_Strain_Traction_X', 'aaa', 'aaa']
variables['Max Strain Traction Y'] = ['h', 'epsilon_2', 'epsilon_Y_t']
formulas['Max Strain Traction Y'] = 'value, epsilon_2 / epsilon_Y_t'
num_vars['Max Strain Traction Y'] = 3
equations['Max Strain Traction Y'] = Max_Strain_Traction_Y
# 
# 
# 
def Max_Strain_Compression_X(solv_vars, vars, dict_val):
    value = vars[0]
    epsilon_1 = vars[1]
    epsilon_X_c = vars[2]

    eq = Eq(value, abs(epsilon_1) / abs(epsilon_X_c))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Strain Compression X')
vars_names['Max Strain Compression X'] = ['Max Strain Compression X', 'aaa', 'aaa']
variables['Max Strain Compression X'] = ['aaa', 'epsilon_1', 'epsilon_X_c']
formulas['Max Strain Compression X'] = 'value = abs(epsilon_1) / abs(epsilon_X_c)'
num_vars['Max Strain Compression X'] = 3
equations['Max Strain Compression X'] = Max_Strain_Compression_X
# 
# 
# 
def Max_Strain_Compression_Y(solv_vars, vars, dict_val):
    value = vars[0]
    epsilon_2 = vars[1]
    epsilon_Y_c = vars[2]

    eq = Eq(value, abs(epsilon_2) / abs(epsilon_Y_c))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Strain Compression Y')
vars_names['Max Strain Compression Y'] = ['Max Strain Compression Y', 'aaa', 'aaa']
variables['Max Strain Compression Y'] = ['aaa', 'epsilon_2', 'epsilon_Y_c']
formulas['Max Strain Compression Y'] = 'value = abs(epsilon_2) / abs(epsilon_Y_c)'
num_vars['Max Strain Compression Y'] = 3
equations['Max Strain Compression Y'] = Max_Strain_Compression_Y
# 
# 
# 
def max_strain_shear(solv_vars, vars, dict_val):
    value = vars[0]
    epsilon_12 = vars[1]
    epsilon_S = vars[2]

    eq = Eq(value, abs(epsilon_12) / epsilon_S)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Max Strain Shear')
vars_names['Max Strain Shear'] = ['Max Strain Shear', 'epsilon_12', 'epsilon_S']
variables['Max Strain Shear'] = ['M_S_S', 'epsilon_12', 'epsilon_S']
formulas['Max Strain Shear'] = 'M.S.S = abs(epsilon_12) / epsilon_S'
num_vars['Max Strain Shear'] = 3
equations['Max Strain Shear'] = max_strain_shear
# 
# 
# 
#interactive failure criteria
def Hoffman_Failure(solv_vars, vars, dict_val):
    value = vars[0]
    sigma_X_t = vars[1]
    sigma_X_c = vars[2]
    sigma_1 = vars[3]
    sigma_Y_t = vars[4]
    sigma_Y_c = vars[5]
    sigma_2 = vars[6]
    sigma_S = vars[7]
    sigma_12 = vars[8]

    eq = Eq(value, (1/sigma_X_t - 1/sigma_X_c) * sigma_1 + \
    (1/(sigma_Y_t - 1/sigma_Y_c)) * sigma_2 + \
    (1/(sigma_X_t * sigma_X_c)) * sigma_1**2 + \
    (1/(sigma_Y_t * sigma_Y_c)) * sigma_2**2 + \
    (1/sigma_S**2) * sigma_12**2 - \
    (1/(sigma_X_t * sigma_X_c)) * sigma_1 * sigma_2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Hoffman Failure')
vars_names['Hoffman Failure'] = ['Hoffman Failure', 'aaa', 'aaa', 'aaa']
variables['Hoffman Failure'] = ['aaa', 'sigma_X_t', 'sigma_X_c', 'sigma_1', 'sigma_Y_t', 'sigma_Y_c', 'sigma_2']
formulas['Hoffman Failure'] = 'value = (1/sigma_X_t - 1/sigma_X_c) * sigma_1 + (1/(sigma_Y_t - 1/sigma_Y_c)) * sigma_2 + (1/(sigma_X_t * sigma_X_c)) * sigma_1**2 + (1/(sigma_Y_t * sigma_Y_c)) * sigma_2**2 + (1/sigma_S**2) * sigma_12**2 - (1/(sigma_X_t * sigma_X_c)) * sigma_1 * sigma_2'
num_vars['Hoffman Failure'] = 7
equations['Hoffman Failure'] = Hoffman_Failure
# 
# 
# 
def  Tsai_Hill_Failure(solv_vars, vars, dict_val):
    value = vars[0]
    sigma_X = vars[1]
    sigma_1 = vars[2]
    sigma_Y = vars[3]
    sigma_2 = vars[4]
    sigma_S = vars[5]
    sigma_12 = vars[6]

    eq = Eq(value, (sigma_1/sigma_X)**2 + (sigma_2/sigma_Y)**2 + (sigma_12/sigma_S)**2 - (sigma_1/sigma_X)*(sigma_2/sigma_X))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Tsai-Hill Failure')
vars_names['Tsai-Hill Failure'] = ['Max Strain Shear', 'lambda_1', 'Temp at 0m', 'aaa']
variables['Tsai-Hill Failure'] = ['h', 'lambda_1', 'T_0', 'T_0_11k']
formulas['Tsai-Hill Failure'] = 'T_0_11k = T_0+lambda_1*h'
num_vars['Tsai-Hill Failure'] = 7
equations['Tsai-Hill Failure'] = Tsai_Hill_Failure
# 
# 
# 