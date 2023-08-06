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
def mach_angle(solv_vars, vars, dict_val):
    mach_angle = vars[0]
    M = vars[1]

    eq = Eq(sin(mach_angle), 1/M)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Mach Angle'
names.append(name)
vars_names[name] = ['Mach Angle', 'Mach']
variables[name] = ['mach_angle', 'M']
formulas[name] = 'sin(mach_angle) = 1/M'
num_vars[name] = len(variables[name])
equations[name] = mach_angle
# 
# 
# 
# stagnation values
def stagnation_enthalpy(solv_vars, vars, dict_val):
    h_t = vars[0]
    h = vars[1]
    gamma = vars[2]
    M = vars[3]

    eq = Eq(h_t, h * (1 + (gamma-1)/2 * M**2))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Stagnation Enthalpy'
names.append(name)
vars_names[name] = ['Stagnation Enthalpy', 'Enthalpy', 'Heat capacity ratio', 'Mach']
variables[name] = ['h_t', 'h', 'gamma', 'M']
formulas[name] = 'h_t = h * (1 + (gamma-1)/2 * M**2)'
num_vars[name] = len(variables[name])
equations[name] = stagnation_enthalpy
# 
# 
# 
def stagnation_temperature(solv_vars, vars, dict_val):
    T_t = vars[0]
    T = vars[1]
    gamma = vars[2]
    M = vars[3]

    eq = Eq(T_t, T * (1 + (gamma-1)/2 * M**2))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Stagnation Temperature'
names.append(name)
vars_names[name] = ['Stagnation Temperature', 'Temperature', 'Heat capacity ratio', 'Mach']
variables[name] = ['T_t', 'T', 'gamma', 'M']
formulas[name] = 'T_t = T * (1 + (gamma-1)/2 * M**2)'
num_vars[name] = len(variables[name])
equations[name] = stagnation_temperature
# 
# 
# 
def stagnation_pressure(solv_vars, vars, dict_val):
    p_t = vars[0]
    p = vars[1]
    gamma = vars[2]
    M = vars[3]

    eq = Eq(p_t, p * (1 + (gamma-1)/2 * M**2)**(gamma/(gamma-1)))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Stagnation Pressure'
names.append(name)
vars_names[name] = ['Stagnation Pressure', 'Pressure', 'Heat capacity ratio', 'Mach']
variables[name] = ['p_t', 'p', 'gamma', 'M']
formulas[name] = 'p_t = p * (1 + (gamma-1)/2 * M**2)**(gamma/(gamma-1))'
num_vars[name] = len(variables[name])
equations[name] = stagnation_pressure
# 
# 
# 
# area variation flow
def area_variation_flow_areas_quotient(solv_vars, vars, dict_val):
    A_2 = vars[0]
    A_1 = vars[1]
    M_1 = vars[2]
    M_2 = vars[2]
    gamma = vars[2]
    delta_S = vars[2]
    R = vars[2]

    eq = Eq(A_2/A_1, M_1/M_2 * ((1 + (gamma - 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_2**2))**((gamma+1)/(2*(gamma-1))) * exp(delta_S/R))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Area Variation Flow: Areas Quotient'
names.append(name)
vars_names[name] = ['Area 1', 'Area 2', 'Mach 1', 'Mach 2', 'Heat capacity ratio', 'Entropy Variation', 'Gas constant']
variables[name] = ['A_1', 'A_2', 'M_1', 'M_2', 'gamma', 'delta_S', 'R']
formulas[name] = 'A_2/A_1 = M_1/M_2 * ((1 + (gamma - 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_2**2))**((gamma+1)/(2*(gamma-1))) * exp(delta_S/R)'
num_vars[name] = len(variables[name])
equations[name] = area_variation_flow_areas_quotient
# 
# 
# 
def area_variation_flow_pressures_quotient(solv_vars, vars, dict_val):
    p_2 = vars[0]
    p_1 = vars[1]
    M_1 = vars[2]
    M_2 = vars[2]
    gamma = vars[2]
    delta_S = vars[2]
    R = vars[2]

    eq = Eq(p_2/p_1, ((1 + (gamma - 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_2**2))**(gamma/(gamma-1)) * exp(delta_S/R))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Area Variation Flow: Pressure Quotient'
names.append(name)
vars_names[name] = ['Pressure 1', 'Pressure 2', 'Mach 1', 'Mach 2', 'Heat capacity ratio', 'Entropy Variation', 'Gas constant']
variables[name] = ['p_1', 'p_2', 'M_1', 'M_2', 'gamma', 'delta_S', 'R']
formulas[name] = 'p_2/p_1 = ((1 + (gamma - 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_2**2))**(gamma/(gamma-1)) * exp(delta_S/R)'
num_vars[name] = len(variables[name])
equations[name] = area_variation_flow_pressures_quotient
# 
# 
# 
def area_variation_flow_densities_quotient(solv_vars, vars, dict_val):
    rho_2 = vars[0]
    rho_1 = vars[1]
    M_1 = vars[2]
    M_2 = vars[2]
    gamma = vars[2]
    delta_S = vars[2]
    R = vars[2]

    eq = Eq(rho_2/rho_1, ((1 + (gamma - 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_2**2))**(gamma/(gamma-1)) * exp(delta_S/R))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Area Variation Flow: Densities Quotient'
names.append(name)
vars_names[name] = ['Density 1', 'Density 2', 'Mach 1', 'Mach 2', 'Heat capacity ratio', 'Entropy Variation', 'Gas constant']
variables[name] = ['rho_1', 'rho_2', 'M_1', 'M_2', 'gamma', 'delta_S', 'R']
formulas[name] = 'rho_2/rho_1 = ((1 + (gamma - 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_2**2))**(gamma/(gamma-1)) * exp(delta_S/R)'
num_vars[name] = len(variables[name])
equations[name] = area_variation_flow_densities_quotient
# 
# 
# 
def area_variation_flow_reference_areas_quotient(solv_vars, vars, dict_val):
    A_2_ref = vars[0]
    A_1_ref = vars[1]
    delta_S = vars[2]
    R = vars[2]

    eq = Eq(A_2_ref/A_1_ref, exp(delta_S/R))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Area Variation Flow: Reference Areas Quotient'
names.append(name)
vars_names[name] = ['Reference Area 1', 'Reference Area 2', 'Entropy Variation', 'Gas constant']
variables[name] = ['A_1_ref', 'A_2_ref', 'delta_S', 'R']
formulas[name] = 'A_2_ref/A_1_ref = exp(delta_S/R)'
num_vars[name] = len(variables[name])
equations[name] = area_variation_flow_reference_areas_quotient
# 
# 
# 
def nozzle_performance_same_pressure(solv_vars, vars, dict_val):
    eta_n = vars[0]
    h_1 = vars[1]
    h_2 = vars[2]
    h_2_S = vars[3]

    eq = Eq(eta_n, (h_1 - h_2)/(h_1 - h_2_S))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'nozzle performance same pressure'
names.append(name)
vars_names[name] = ['aaa', 'aaa', 'aaa']
variables[name] = ['eta_n', 'h_1', 'h_2', 'h_2_S']
formulas[name] = 'eta_n = (h_1 - h_2)/(h_1 - h_2_S)'
num_vars[name] = len(variables[name])
equations[name] = nozzle_performance_same_pressure
# 
# 
# 
# normal shock
def normal_shock_mach(solv_vars, vars, dict_val):
    M2 = vars[0]
    M1 = vars[1]
    gamma = vars[2]

    eq = Eq(M2, sqrt((M1**2 * (gamma-1) + 2)/(2*gamma+M1**2-(gamma-1))))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Normal Shock Mach'
names.append(name)
vars_names[name] = ['Mach after shock', 'Mach before shock', 'Specific Heat ratio']
variables[name] = ['M2', 'M1', 'gamma']
formulas[name] = 'M2 = sqrt((M1**2 * (gamma-1) + 2)/(2*gamma+M1**2-(gamma-1)))'
num_vars[name] = len(variables[name])
equations[name] = normal_shock_mach
# 
# 
# 
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(T_1 * (1 + (gamma-1)/2 * M_1**2), T_2 * (1 + (gamma-1)/2 * M_2**2))

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
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(p_1 * (1 + gamma * M_1**2), p_2 * (1 + gamma * M_2**2))

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
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(M_2, sqrt((M_1**2 + 2/(gamma-1)) / ((2 * gamma)/(gamma-1) * M_1**2 - 1)))

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
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq(p_t_1/p_t_2 - (((gamma + 1)/2 * M_1**2)/(1 + (gamma - 1)/2 * M_1**2))**(gamma/(gamma - 1)) * ((2 * gamma)/(gamma + 1) * M_1**2 - (gamma - 1)/(gamma + 1))**(1/(1 - gamma)))

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
def aaa(solv_vars, vars, dict_val):
    aaa = vars[0]
    aaa = vars[1]
    aaa = vars[2]

    eq = Eq((V_1 - V_2)/a_1 - (2/(gamma + 1)) * ((M_1**2 - 1)/M_1))

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











def relative_roughness(sol_var, rel_roughness, epsilon, D):
    expr_1 = rel_roughness - epsilon/D
    
    solution = solve(expr_1, sol_var)
    
    return solution



def friction_factor(sol_var, Re, rel_roughness):
    if Re < 3000:
        expr_1 = f_D - 64/Re
    else:
        expr_1 = 10**(-1/(2*sqrt(f_D))) - (rel_roughness/3.7 + 2.51/(Re * sqrt(f_D)))
    
    solution = solve(expr_1, sol_var)
    
    return solution









# choques moveis e obliquos
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
expression_1 = M_1_n - M_1 * sin(theta)

expression_2 = M_2_n - M_2 * sin(theta - delta)

expression_3 = rho_2/rho_1 - ((gamma+1) * M_1_n**2)/((gamma-1) * M_1_n**2 + 2)

expression_4 = rho_2/rho_1 - V_1_n/V_2_n

expression_5 = rho_2/rho_1 - (tan(theta))/(tan(theta - delta))

expression_6 = V_1_n/V_2_n - ((gamma + 1) * M_1**2 * (sin(theta))**2) / ((gamma - 1) * M_1**2 * (sin(theta))**2 + 2)

#expression_4 = tan(delta) - 2 * cot(theta) * ((M_1**2 * (sin(theta))**2 - 1)/(M_1**2 * (gamma + cos(2*theta)) + 2))




# escoamento de prandtl-meyer
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq((p_2 - p_1)/p_1, (2 * gamma)/(gamma + 1) * (M_1**2 - 1))

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = '(p_2 - p_1)/p_1 = (2 * gamma)/(gamma + 1) * (M_1**2 - 1)'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(nu, ((gamma+1)/(gamma-1))**(1/2) * (atan(((gamma-1)/(gamma+1) * (M_1**2 - 1))))**(1/2) - (atan(M**2 - 1))**(1/2))

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = 'nu = ((gamma+1)/(gamma-1))**(1/2) * (atan(((gamma-1)/(gamma+1) * (M**2 - 1))))**(1/2) - (atan(M_1**2 - 1))**(1/2)'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq((s_2-s_1)/gas_constant, (2 * gamma * (M_1**2-1)**3)/(3*(gamma+1)**2))

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = '(s_2-s_1)/gas_constant = (2 * gamma * (M_1**2-1)**3)/(3*(gamma+1)**2)'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 
# fanno flow
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(G, rho * V)

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = 'G = rho * V'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(h_t, h + G**2/(2 * rho**2))

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = 'h_t = h + G**2/(2 * rho**2)'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq((p_1 + rho_1 * V_1**2) - F_f/A, p_2 + rho_2 * V_2**2)

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = '(p_1 + rho_1 * V_1**2) - F_f/A = p_2 + rho_2 * V_2**2'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 
# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(T_2/T_1, (1+(gamma-1)/2*M_1**2)/(1+(gamma-1)/2*M_2**2))

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = 'T_2/T_1 = (1+(gamma-1)/2*M_1**2)/(1+(gamma-1)/2*M_2**2)'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 