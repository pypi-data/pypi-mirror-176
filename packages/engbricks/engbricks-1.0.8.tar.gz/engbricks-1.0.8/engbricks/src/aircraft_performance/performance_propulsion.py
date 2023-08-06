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
def Thust_Specific_Fuel_Consumption(solv_vars, vars, dict_val):
	T = vars[0]
	TSFC = vars[1]
	g = vars[2]
	m_dot_f = vars[3]

	eq = Eq(TSFC, m_dot_f*g/T)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Thust Specific Fuel Consumption')
vars_names['Thust Specific Fuel Consumption'] = ['Thrust', 'Thrust Specific Fuel Consumption', 'Gravity Acc', 'Fuel flow']
variables['Thust Specific Fuel Consumption'] = ['T', 'TSFC', 'g', 'm_dot_f']
formulas['Thust Specific Fuel Consumption'] = 'TSFC = m_dot_f*g/T'
num_vars['Thust Specific Fuel Consumption'] = 4
equations['Thust Specific Fuel Consumption'] = Thust_Specific_Fuel_Consumption
# 
# 
# 
def Power_Specific_Fuel_Consumption(solv_vars, vars, dict_val):
	PSFC = vars[0]
	P_e = vars[1]
	g = vars[2]
	m_dot_f = vars[3]

	eq = Eq(PSFC, m_dot_f*g/P_e)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Power Specific Fuel Consumption')
vars_names['Power Specific Fuel Consumption'] = ['Power Specific Fuel Consumption', 'Power effective', 'Gravity Acc', 'Fuel flow']
variables['Power Specific Fuel Consumption'] = ['PSFC', 'P_e', 'g', 'm_dot_f']
formulas['Power Specific Fuel Consumption'] = 'PSFC = m_dot_f*g/P_e'
num_vars['Power Specific Fuel Consumption'] = 4
equations['Power Specific Fuel Consumption'] = Power_Specific_Fuel_Consumption
# 
# 
# 
def TSFC_and_PSFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	TSFC = vars[1]
	V = vars[2]
	eta_p = vars[3]

	eq = Eq(TSFC, V*(eta_p)*PSFC)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('TSFC and PSFC')
vars_names['TSFC and PSFC'] = ['Power Specific Fuel Consumption', 'Thrust Specific Fuel Consumption', 'Speed', 'Populsive Efficiency']
variables['TSFC and PSFC'] = ['PSFC', 'TSFC', 'V', 'eta_p']
formulas['TSFC and PSFC'] = 'TSFC = V*(eta_p)*PSFC'
num_vars['TSFC and PSFC'] = 4
equations['TSFC and PSFC'] = TSFC_and_PSFC
# 
# 
# 
def Piston_Air_Suck(solv_vars, vars, dict_val):
	P_e = vars[0]
	P_e_0 = vars[1]
	delta = vars[2]
	rho = vars[3]
	rho_0 = vars[4]

	eq = Eq(P_e, P_e_0*delta*(rho/rho_0))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Piston Air Suck')
vars_names['Piston Air Suck'] = ['Power effective', 'Power effective s.l.', 'Accelerator', 'Air Density', 'Air Density Sea Level']
variables['Piston Air Suck'] = ['P_e', 'P_e_0', 'delta', 'rho', 'rho_0']
formulas['Piston Air Suck'] = 'P_e = P_e_0*delta*(rho/rho_0)'
num_vars['Piston Air Suck'] = 5
equations['Piston Air Suck'] = Piston_Air_Suck
# 
# 
# 
def Piston_Air_Suck_SFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	PSFC_0 = vars[1]

	eq = Eq(PSFC, PSFC_0)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Piston Air Suck SFC')
vars_names['Piston Air Suck SFC'] = ['Power Specific Fuel Consumption', 'Power Specific Fuel Consumption s.l.']
variables['Piston Air Suck SFC'] = ['PSFC', 'PSFC_0']
formulas['Piston Air Suck SFC'] = 'PSFC = PSFC_0'
num_vars['Piston Air Suck SFC'] = 2
equations['Piston Air Suck SFC'] = Piston_Air_Suck_SFC
# 
# 
# 
def Piston_Turbo_h_lower_h_cr(solv_vars, vars, dict_val):
	P_e = vars[0]
	P_e_0 = vars[1]
	delta = vars[2]

	eq = Eq(P_e, P_e_0*delta)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Piston Turbo h<h_cr')
vars_names['Piston Turbo h<h_cr'] = ['Power effective', 'Power effective s.l.', 'Accelerator']
variables['Piston Turbo h<h_cr'] = ['P_e', 'P_e_0', 'delta']
formulas['Piston Turbo h<h_cr'] = 'P_e = P_e_0*delta'
num_vars['Piston Turbo h<h_cr'] = 3
equations['Piston Turbo h<h_cr'] = Piston_Turbo_h_lower_h_cr
# 
# 
# 
def Piston_Turbo_h_higher_h_cr(solv_vars, vars, dict_val):
    P_e = vars[0]
    P_e_0 = vars[1]
    delta = vars[2]
    rho = vars[3]
    rho_cr = vars[4]

    eq = Eq(P_e, P_e_0*delta*(rho/rho_cr))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Piston Turbo h>h_cr')
vars_names['Piston Turbo h>h_cr'] = ['Power effective', 'Power effective s.l.', 'Accelerator', 'Air Density', 'Air Density Critical']
variables['Piston Turbo h>h_cr'] = ['P_e', 'P_e_0', 'delta', 'rho', 'rho_cr']
formulas['Piston Turbo h>h_cr'] = 'P_e = P_e_0*delta*(rho/rho_cr)'
num_vars['Piston Turbo h>h_cr'] = 5
equations['Piston Turbo h>h_cr'] = Piston_Turbo_h_higher_h_cr
# 
# 
# 
def Piston_Turbo_SFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	PSFC_0 = vars[1]

	eq = Eq(PSFC, PSFC_0)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Piston Turbo SFC')
vars_names['Piston Turbo SFC'] = ['Power Specific Fuel Consumption', 'Power Specific Fuel Consumption s.l.']
variables['Piston Turbo SFC'] = ['PSFC', 'PSFC_0']
formulas['Piston Turbo SFC'] = 'PSFC = PSFC_0'
num_vars['Piston Turbo SFC'] = 2
equations['Piston Turbo SFC'] = Piston_Turbo_SFC
# 
# 
# 
def Turboprop(solv_vars, vars, dict_val):
	P_e = vars[0]
	P_e_0 = vars[1]
	delta = vars[2]
	rho = vars[3]
	rho_0 = vars[4]

	eq = Eq(P_e, P_e_0*delta*(rho/rho_0))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turboprop')
vars_names['Turboprop'] = ['Power effective', 'Power effective s.l.', 'Accelerator', 'Air Density', 'Air Density Sea Level']
variables['Turboprop'] = ['P_e', 'P_e_0', 'delta', 'rho', 'rho_0']
formulas['Turboprop'] = 'P_e = P_e_0*delta*(rho/rho_0)'
num_vars['Turboprop'] = 5
equations['Turboprop'] = Turboprop
# 
# 
# 
def Turboprop_SFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	PSFC_0 = vars[1]
	delta = vars[2]

	eq = Eq(PSFC, PSFC_0*(1/delta)**0.5)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turboprop SFC')
vars_names['Turboprop SFC'] = ['Power Specific Fuel Consumption', 'Power Specific Fuel Consumption s.l.', 'Accelerator']
variables['Turboprop SFC'] = ['PSFC', 'PSFC_0', 'delta']
formulas['Turboprop SFC'] = 'PSFC = PSFC_0*(1/delta)**0.5'
num_vars['Turboprop SFC'] = 3
equations['Turboprop SFC'] = Turboprop_SFC
# 
# 
# 
def Turbofan_high_lambda(solv_vars, vars, dict_val):
	M = vars[0]
	M_ref = vars[1]
	T = vars[2]
	T_0 = vars[3]
	delta = vars[4]
	rho = vars[5]
	rho_0 = vars[6]

	eq = Eq(T, (M_ref/M)**exp(M)*T_0*delta*(rho/rho_0))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbofan high lambda')
vars_names['Turbofan high lambda'] = ['Mach', 'Reference Mach', 'Thrust', 'Thrust s.l.', 'Accelerator', 'Air Density', 'Air Density Sea Level']
variables['Turbofan high lambda'] = ['M', 'M_ref', 'T', 'T_0', 'delta', 'rho', 'rho_0']
formulas['Turbofan high lambda'] = 'T = (M_ref/M)**exp(M)*T_0*delta*(rho/rho_0)'
num_vars['Turbofan high lambda'] = 7
equations['Turbofan high lambda'] = Turbofan_high_lambda
# 
# 
# 
def Turbofan_high_lambda_SFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	PSFC_0 = vars[1]
	delta = vars[2]

	eq = Eq(PSFC, PSFC_0*(1/delta)**0.5)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbofan high lambda SFC')
vars_names['Turbofan high lambda SFC'] = ['Power Specific Fuel Consumption', 'Power Specific Fuel Consumption s.l.', 'Accelerator']
variables['Turbofan high lambda SFC'] = ['PSFC', 'PSFC_0', 'delta']
formulas['Turbofan high lambda SFC'] = 'PSFC = PSFC_0*(1/delta)**0.5'
num_vars['Turbofan high lambda SFC'] = 3
equations['Turbofan high lambda SFC'] = Turbofan_high_lambda_SFC
# 
# 
# 
def Turbofan_low_lambda_h_lower_h_11k(solv_vars, vars, dict_val):
	T = vars[0]
	T_0 = vars[1]
	delta = vars[2]
	rho = vars[3]
	rho_0 = vars[4]

	eq = Eq(T, T_0*delta*(rho/rho_0)**0.7)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbofan low lambda h<h_11k')
vars_names['Turbofan low lambda h<h_11k'] = ['Thrust', 'Thrust s.l.', 'Accelerator', 'Air Density', 'Air Density Sea Level']
variables['Turbofan low lambda h<h_11k'] = ['T', 'T_0', 'delta', 'rho', 'rho_0']
formulas['Turbofan low lambda h<h_11k'] = 'T = T_0*delta*(rho/rho_0)**0.7'
num_vars['Turbofan low lambda h<h_11k'] = 5
equations['Turbofan low lambda h<h_11k'] = Turbofan_low_lambda_h_lower_h_11k
# 
# 
# 
def Turbofan_low_lambda_h_higher_h_11k(solv_vars, vars, dict_val):
    T = vars[0]
    T_0 = vars[1]
    delta = vars[2]
    sigma = vars[3]
    sigma_11km = vars[4]

    eq = Eq(T, T_0*delta*(sigma/sigma_11km**0.3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append('Turbofan low lambda h>11_k')
vars_names['Turbofan low lambda h>11_k'] = ['Thrust', 'Thrust s.l.', 'Accelerator', 'sigma', 'sigma 11km']
variables['Turbofan low lambda h>11_k'] = ['T', 'T_0', 'delta', 'sigma', 'sigma_11km']
formulas['Turbofan low lambda h>11_k'] = 'T = T_0*delta*(sigma/sigma_11km**0.3)'
num_vars['Turbofan low lambda h>11_k'] = 5
equations['Turbofan low lambda h>11_k'] = Turbofan_low_lambda_h_higher_h_11k
# 
# 
# 
def Turbofan_low_lambda_SFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	PSFC_0 = vars[1]
	delta = vars[2]

	eq = Eq(PSFC, PSFC_0*(1/delta)**0.5)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbofan low lambda SFC')
vars_names['Turbofan low lambda SFC'] = ['Power Specific Fuel Consumption', 'Power Specific Fuel Consumption s.l.', 'Accelerator']
variables['Turbofan low lambda SFC'] = ['PSFC', 'PSFC_0', 'delta']
formulas['Turbofan low lambda SFC'] = 'PSFC = PSFC_0*(1/delta)**0.5'
num_vars['Turbofan low lambda SFC'] = 3
equations['Turbofan low lambda SFC'] = Turbofan_low_lambda_SFC
# 
# 
# 
def Turbofan_low_lambda_with_afterburn(solv_vars, vars, dict_val):
	M = vars[0]
	T = vars[1]
	T_0 = vars[2]
	delta = vars[3]
	rho = vars[4]
	rho_0 = vars[5]

	eq = Eq(T, T_0*delta*(rho/rho_0)*(1+0.7*M))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbofan low lambda with afterburn')
vars_names['Turbofan low lambda with afterburn'] = ['Mach', 'Thrust', 'Thrust s.l.', 'Accelerator', 'Air Density', 'Air Density Sea Level']
variables['Turbofan low lambda with afterburn'] = ['M', 'T', 'T_0', 'delta', 'rho', 'rho_0']
formulas['Turbofan low lambda with afterburn'] = 'T = T_0*delta*(rho/rho_0)*(1+0.7*M)'
num_vars['Turbofan low lambda with afterburn'] = 6
equations['Turbofan low lambda with afterburn'] = Turbofan_low_lambda_with_afterburn
# 
# 
# 
def Turbofan_low_lambda__with_afterburn_SFC(solv_vars, vars, dict_val):
	PSFC = vars[0]
	PSFC_0 = vars[1]
	delta = vars[2]

	eq = Eq(PSFC, PSFC_0*(1/delta)**0.5)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbofan low lambda  with afterburn SFC')
vars_names['Turbofan low lambda  with afterburn SFC'] = ['Power Specific Fuel Consumption', 'Power Specific Fuel Consumption s.l.', 'Accelerator']
variables['Turbofan low lambda  with afterburn SFC'] = ['PSFC', 'PSFC_0', 'delta']
formulas['Turbofan low lambda  with afterburn SFC'] = 'PSFC = PSFC_0*(1/delta)**0.5'
num_vars['Turbofan low lambda  with afterburn SFC'] = 3
equations['Turbofan low lambda  with afterburn SFC'] = Turbofan_low_lambda__with_afterburn_SFC
# 
# 
# 
def Fuel_Fraction(solv_vars, vars, dict_val):
	W = vars[0]
	W_fuel = vars[1]
	zeta = vars[2]

	eq = Eq(zeta, W_fuel/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Fuel Fraction')
vars_names['Fuel Fraction'] = ['Weight', 'Fuel Weight', 'Fuel Weight ratio']
variables['Fuel Fraction'] = ['W', 'W_fuel', 'zeta']
formulas['Fuel Fraction'] = 'zeta = W_fuel/W'
num_vars['Fuel Fraction'] = 3
equations['Fuel Fraction'] = Fuel_Fraction
# 
# 
# 
