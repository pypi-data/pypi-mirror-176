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
def Jet_Range_V_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	TSFC = vars[1]
	V = vars[2]
	zeta = vars[3]
	X_V_C_L = vars[4]

	eq = Eq(X_V_C_L, V*E/TSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Range V_C_L')
vars_names['Jet Range V_C_L'] = ['Efficiency', 'Thrust Specific Fuel Consumption', 'Speed', 'Fuel Weight ratio', 'Range V-C_L']
variables['Jet Range V_C_L'] = ['E', 'TSFC', 'V', 'zeta', 'X_V_C_L']
formulas['Jet Range V_C_L'] = 'X_V_C_L = V*E/TSFC*ln(1/(1-zeta))'
num_vars['Jet Range V_C_L'] = 5
equations['Jet Range V_C_L'] = Jet_Range_V_C_L
# 
# 
# 
def Jet_Range_H_C_L(solv_vars, vars, dict_val):
	E_1 = vars[0]
	TSFC = vars[1]
	V_1 = vars[2]
	zeta = vars[3]
	X_h_C_L = vars[4]

	eq = Eq(X_h_C_L, 2*V_1*E_1/TSFC*(1-sqrt(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Range H_C_L')
vars_names['Jet Range H_C_L'] = ['Initial Efficiency', 'Thrust Specific Fuel Consumption', 'Cruise Initial Speed', 'Fuel Weight ratio', 'Range h-C_L']
variables['Jet Range H_C_L'] = ['E_1', 'TSFC', 'V_1', 'zeta', 'X_h_C_L']
formulas['Jet Range H_C_L'] = 'X_h_C_L = 2*V_1*E_1/TSFC*(1-sqrt(1-zeta))'
num_vars['Jet Range H_C_L'] = 5
equations['Jet Range H_C_L'] = Jet_Range_H_C_L
# 
# 
# 
def Jet_Range_h_V(solv_vars, vars, dict_val):
	E_1 = vars[0]
	E_max = vars[1]
	K = vars[2]
	TSFC = vars[3]
	V = vars[4]
	zeta = vars[5]
	X_h_V = vars[6]
	C_L_1 = vars[7]

	eq = Eq(X_h_V, 2*V*E_max/TSFC*arctg((E_1*zeta)/(2*E_max*(1-K*E_1*C_L_1*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Range h_V')
vars_names['Jet Range h_V'] = ['Initial Efficiency', 'Max Efficiency', 'Induced Drag Factor', 'Thrust Specific Fuel Consumption', 'Speed', 'Fuel Weight ratio', 'Range h-V', 'Cruise Initial C_L']
variables['Jet Range h_V'] = ['E_1', 'E_max', 'K', 'TSFC', 'V', 'zeta', 'X_h_V', 'C_L_1']
formulas['Jet Range h_V'] = 'X_h_V = 2*V*E_max/TSFC*arctg((E_1*zeta)/(2*E_max*(1-K*E_1*C_L_1*zeta)))'
num_vars['Jet Range h_V'] = 8
equations['Jet Range h_V'] = Jet_Range_h_V
# 
# 
# 
def Efficiency_Cruise_Beginning(solv_vars, vars, dict_val):
	E_1 = vars[0]
	C_L_1 = vars[1]
	C_D_1 = vars[2]

	eq = Eq(E_1, C_L_1/C_D_1)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Efficiency Cruise Beginning')
vars_names['Efficiency Cruise Beginning'] = ['Initial Efficiency', 'Cruise Initial C_L', 'Cruise Initial C_D']
variables['Efficiency Cruise Beginning'] = ['E_1', 'C_L_1', 'C_D_1']
formulas['Efficiency Cruise Beginning'] = 'E_1 = C_L_1/C_D_1'
num_vars['Efficiency Cruise Beginning'] = 3
equations['Efficiency Cruise Beginning'] = Efficiency_Cruise_Beginning
# 
# 
# 
def V_br_1(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_br_1 = vars[3]
	W_1 = vars[4]
	rho = vars[5]
	sigma = vars[6]

	eq = Eq(V_br_1, sqrt(W_1/(0.5*rho*sigma*S))*(3*K/C_D0)**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('V_br_1')
vars_names['V_br_1'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Best Range Initial Speed', 'Cruise Initial Weight', 'Air Density', 'sigma']
variables['V_br_1'] = ['C_D0', 'K', 'S', 'V_br_1', 'W_1', 'rho', 'sigma']
formulas['V_br_1'] = 'V_br_1 = sqrt(W_1/(0.5*rho*sigma*S))*(3*K/C_D0)**1/4'
num_vars['V_br_1'] = 7
equations['V_br_1'] = V_br_1
# 
# 
# 
def Jet_Best_Range_V_C_L(solv_vars, vars, dict_val):
	TSFC = vars[0]
	zeta = vars[1]
	X_br_V_C_L = vars[2]
	V_br = vars[3]
	E_br = vars[4]

	eq = Eq(X_br_V_C_L, V_br*E_br/TSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range V_C_L')
vars_names['Jet Best Range V_C_L'] = ['Thrust Specific Fuel Consumption', 'Fuel Weight ratio', 'Best Range V-C_L', 'Best Range Speed', 'Best Range Efficiency']
variables['Jet Best Range V_C_L'] = ['TSFC', 'zeta', 'X_br_V_C_L', 'V_br', 'E_br']
formulas['Jet Best Range V_C_L'] = 'X_br_V_C_L = V_br*E_br/TSFC*ln(1/(1-zeta))'
num_vars['Jet Best Range V_C_L'] = 5
equations['Jet Best Range V_C_L'] = Jet_Best_Range_V_C_L
# 
# 
# 
def Jet_Best_Range_h_V(solv_vars, vars, dict_val):
	E_max = vars[0]
	K = vars[1]
	TSFC = vars[2]
	zeta = vars[3]
	V_br = vars[4]
	E_br = vars[5]
	X_h_V = vars[6]
	C_L_br = vars[7]

	eq = Eq(X_h_V, 2*V_br*E_max/TSFC*arctg((E_br*zeta)/(2*E_max*(1-K*E_br*C_L_br*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range h_V')
vars_names['Jet Best Range h_V'] = ['Max Efficiency', 'Induced Drag Factor', 'Thrust Specific Fuel Consumption', 'Fuel Weight ratio', 'Best Range Speed', 'Best Range Efficiency', 'Range h-V', 'Best Range C_L']
variables['Jet Best Range h_V'] = ['E_max', 'K', 'TSFC', 'zeta', 'V_br', 'E_br', 'X_h_V', 'C_L_br']
formulas['Jet Best Range h_V'] = 'X_h_V = 2*V_br*E_max/TSFC*arctg((E_br*zeta)/(2*E_max*(1-K*E_br*C_L_br*zeta)))'
num_vars['Jet Best Range h_V'] = 8
equations['Jet Best Range h_V'] = Jet_Best_Range_h_V
# 
# 
# 
def Jet_Best_Range_h_C_L(solv_vars, vars, dict_val):
	TSFC = vars[0]
	V_br_1 = vars[1]
	zeta = vars[2]
	X_br_h_C_L = vars[3]
	E_br = vars[4]

	eq = Eq(X_br_h_C_L, 2*V_br_1*E_br/TSFC*(1-sqrt(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range h_C_L')
vars_names['Jet Best Range h_C_L'] = ['Thrust Specific Fuel Consumption', 'Best Range Initial Speed', 'Fuel Weight ratio', 'Best Range h-C_L', 'Best Range Efficiency']
variables['Jet Best Range h_C_L'] = ['TSFC', 'V_br_1', 'zeta', 'X_br_h_C_L', 'E_br']
formulas['Jet Best Range h_C_L'] = 'X_br_h_C_L = 2*V_br_1*E_br/TSFC*(1-sqrt(1-zeta))'
num_vars['Jet Best Range h_C_L'] = 5
equations['Jet Best Range h_C_L'] = Jet_Best_Range_h_C_L
# 
# 
# 
def Jet_Best_Range_Lift_Coefficient(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	C_L_br = vars[2]

	eq = Eq(C_L_br, sqrt(C_D0/(3*K)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range Lift Coefficient')
vars_names['Jet Best Range Lift Coefficient'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Best Range C_L']
variables['Jet Best Range Lift Coefficient'] = ['C_D0', 'K', 'C_L_br']
formulas['Jet Best Range Lift Coefficient'] = 'C_L_br = sqrt(C_D0/(3*K))'
num_vars['Jet Best Range Lift Coefficient'] = 3
equations['Jet Best Range Lift Coefficient'] = Jet_Best_Range_Lift_Coefficient
# 
# 
# 
def Jet_Best_Range_Drag_Coefficient(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	C_D_br = vars[1]

	eq = Eq(C_D_br, 4/3*C_D0)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range Drag Coefficient')
vars_names['Jet Best Range Drag Coefficient'] = ['Parasite Drag Coefficient', 'Best Range C_D']
variables['Jet Best Range Drag Coefficient'] = ['C_D0', 'C_D_br']
formulas['Jet Best Range Drag Coefficient'] = 'C_D_br = 4/3*C_D0'
num_vars['Jet Best Range Drag Coefficient'] = 2
equations['Jet Best Range Drag Coefficient'] = Jet_Best_Range_Drag_Coefficient
# 
# 
# 
def Jet_Best_Range_Efficiency(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	E_br = vars[2]

	eq = Eq(E_br, sqrt(3/(16*K*C_D0)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range Efficiency')
vars_names['Jet Best Range Efficiency'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Best Range Efficiency']
variables['Jet Best Range Efficiency'] = ['C_D0', 'K', 'E_br']
formulas['Jet Best Range Efficiency'] = 'E_br = sqrt(3/(16*K*C_D0))'
num_vars['Jet Best Range Efficiency'] = 3
equations['Jet Best Range Efficiency'] = Jet_Best_Range_Efficiency
# 
# 
# 
def Jet_Best_Range_Speed(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	W = vars[3]
	rho_0 = vars[4]
	sigma = vars[5]
	V_br = vars[6]

	eq = Eq(V_br, sqrt(2/(rho_0*sigma)*W/S)*(3*K/C_D0)**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Range Speed')
vars_names['Jet Best Range Speed'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Weight', 'Air Density Sea Level', 'sigma', 'Best Range Speed']
variables['Jet Best Range Speed'] = ['C_D0', 'K', 'S', 'W', 'rho_0', 'sigma', 'V_br']
formulas['Jet Best Range Speed'] = 'V_br = sqrt(2/(rho_0*sigma)*W/S)*(3*K/C_D0)**1/4'
num_vars['Jet Best Range Speed'] = 7
equations['Jet Best Range Speed'] = Jet_Best_Range_Speed
# 
# 
# 
def Jet_Endurance_h_V(solv_vars, vars, dict_val):
	E_1 = vars[0]
	E_max = vars[1]
	K = vars[2]
	TSFC = vars[3]
	t_h_V = vars[4]
	zeta = vars[5]
	C_L_1 = vars[6]

	eq = Eq(t_h_V, 2*E_max/TSFC*arctg(E_1*zeta/(2*E_max*(1-K*E_1*C_L_1*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Endurance h_V')
vars_names['Jet Endurance h_V'] = ['Initial Efficiency', 'Max Efficiency', 'Induced Drag Factor', 'Thrust Specific Fuel Consumption', 'Endurance h-V', 'Fuel Weight ratio', 'Cruise Initial C_L']
variables['Jet Endurance h_V'] = ['E_1', 'E_max', 'K', 'TSFC', 't_h_V', 'zeta', 'C_L_1']
formulas['Jet Endurance h_V'] = 't_h_V = 2*E_max/TSFC*arctg(E_1*zeta/(2*E_max*(1-K*E_1*C_L_1*zeta)))'
num_vars['Jet Endurance h_V'] = 7
equations['Jet Endurance h_V'] = Jet_Endurance_h_V
# 
# 
# 
def Jet_Endurance_V_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	TSFC = vars[1]
	t_V_C_L = vars[2]
	zeta = vars[3]

	eq = Eq(t_V_C_L, E/TSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Endurance V_C_L')
vars_names['Jet Endurance V_C_L'] = ['Efficiency', 'Thrust Specific Fuel Consumption', 'Endurance V-C_L', 'Fuel Weight ratio']
variables['Jet Endurance V_C_L'] = ['E', 'TSFC', 't_V_C_L', 'zeta']
formulas['Jet Endurance V_C_L'] = 't_V_C_L = E/TSFC*ln(1/(1-zeta))'
num_vars['Jet Endurance V_C_L'] = 4
equations['Jet Endurance V_C_L'] = Jet_Endurance_V_C_L
# 
# 
# 
def Jet_Endurance_h_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	TSFC = vars[1]
	t_h_C_L = vars[2]
	zeta = vars[3]

	eq = Eq(t_h_C_L, E/TSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Endurance h_C_L')
vars_names['Jet Endurance h_C_L'] = ['Efficiency', 'Thrust Specific Fuel Consumption', 'Endurance h-C_L', 'Fuel Weight ratio']
variables['Jet Endurance h_C_L'] = ['E', 'TSFC', 't_h_C_L', 'zeta']
formulas['Jet Endurance h_C_L'] = 't_h_C_L = E/TSFC*ln(1/(1-zeta))'
num_vars['Jet Endurance h_C_L'] = 4
equations['Jet Endurance h_C_L'] = Jet_Endurance_h_C_L
# 
# 
# 
def Jet_Best_Endurance_Lift_Coefficient(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	C_L_be = vars[2]

	eq = Eq(C_L_be, sqrt(C_D0/K))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Endurance Lift Coefficient')
vars_names['Jet Best Endurance Lift Coefficient'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Best Endurance C_L']
variables['Jet Best Endurance Lift Coefficient'] = ['C_D0', 'K', 'C_L_be']
formulas['Jet Best Endurance Lift Coefficient'] = 'C_L_be = sqrt(C_D0/K)'
num_vars['Jet Best Endurance Lift Coefficient'] = 3
equations['Jet Best Endurance Lift Coefficient'] = Jet_Best_Endurance_Lift_Coefficient
# 
# 
# 
def Jet_Best_Endurance_Speed(solv_vars, vars, dict_val):
	V_D_min = vars[0]
	V_be = vars[1]

	eq = Eq(V_be, V_D_min)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Endurance Speed')
vars_names['Jet Best Endurance Speed'] = ['Min Drag Speed', 'Best Endurance Speed']
variables['Jet Best Endurance Speed'] = ['V_D_min', 'V_be']
formulas['Jet Best Endurance Speed'] = 'V_be = V_D_min'
num_vars['Jet Best Endurance Speed'] = 2
equations['Jet Best Endurance Speed'] = Jet_Best_Endurance_Speed
# 
# 
# 
def Jet_Best_Endurance_Efficiency(solv_vars, vars, dict_val):
	E_be = vars[0]
	E_max = vars[1]

	eq = Eq(E_be, E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Endurance Efficiency')
vars_names['Jet Best Endurance Efficiency'] = ['Best Endurance Efficiency', 'Max Efficiency']
variables['Jet Best Endurance Efficiency'] = ['E_be', 'E_max']
formulas['Jet Best Endurance Efficiency'] = 'E_be = E_max'
num_vars['Jet Best Endurance Efficiency'] = 2
equations['Jet Best Endurance Efficiency'] = Jet_Best_Endurance_Efficiency
# 
# 
# 
def Jet_Best_Endurance_h_V(solv_vars, vars, dict_val):
	C_L_min_D = vars[0]
	E_max = vars[1]
	K = vars[2]
	TSFC = vars[3]
	t_be_h_V = vars[4]
	zeta = vars[5]

	eq = Eq(t_be_h_V, 2*E_max/TSFC*arctg((E_max*zeta)/(2*E_max(1-K*E_max*C_L_min_D*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Endurance h_V')
vars_names['Jet Best Endurance h_V'] = ['Min Drag C_L', 'Max Efficiency', 'Induced Drag Factor', 'Thrust Specific Fuel Consumption', 'Best Endurance h-V', 'Fuel Weight ratio']
variables['Jet Best Endurance h_V'] = ['C_L_min_D', 'E_max', 'K', 'TSFC', 't_be_h_V', 'zeta']
formulas['Jet Best Endurance h_V'] = 't_be_h_V = 2*E_max/TSFC*arctg((E_max*zeta)/(2*E_max(1-K*E_max*C_L_min_D*zeta)))'
num_vars['Jet Best Endurance h_V'] = 6
equations['Jet Best Endurance h_V'] = Jet_Best_Endurance_h_V
# 
# 
# 
def Jet_Best_Endurance_V_C_L(solv_vars, vars, dict_val):
	E_max = vars[0]
	TSFC = vars[1]
	t_be_V_C_L = vars[2]
	zeta = vars[3]

	eq = Eq(t_be_V_C_L, E_max/TSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Endurance V_C_L')
vars_names['Jet Best Endurance V_C_L'] = ['Max Efficiency', 'Thrust Specific Fuel Consumption', 'Best Endurance V-C_L', 'Fuel Weight ratio']
variables['Jet Best Endurance V_C_L'] = ['E_max', 'TSFC', 't_be_V_C_L', 'zeta']
formulas['Jet Best Endurance V_C_L'] = 't_be_V_C_L = E_max/TSFC*ln(1/(1-zeta))'
num_vars['Jet Best Endurance V_C_L'] = 4
equations['Jet Best Endurance V_C_L'] = Jet_Best_Endurance_V_C_L
# 
# 
# 
def Jet_Best_Endurance_h_C_L(solv_vars, vars, dict_val):
	E_max = vars[0]
	TSFC = vars[1]
	t_be_h_C_L = vars[2]
	zeta = vars[3]

	eq = Eq(t_be_h_C_L, E_max/TSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Best Endurance h_C_L')
vars_names['Jet Best Endurance h_C_L'] = ['Max Efficiency', 'Thrust Specific Fuel Consumption', 'Best Endurance h-C_L', 'Fuel Weight ratio']
variables['Jet Best Endurance h_C_L'] = ['E_max', 'TSFC', 't_be_h_C_L', 'zeta']
formulas['Jet Best Endurance h_C_L'] = 't_be_h_C_L = E_max/TSFC*ln(1/(1-zeta))'
num_vars['Jet Best Endurance h_C_L'] = 4
equations['Jet Best Endurance h_C_L'] = Jet_Best_Endurance_h_C_L
# 
# 
# 
