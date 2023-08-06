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
def Propeller_Range_h_V(solv_vars, vars, dict_val):
	E_1 = vars[0]
	E_max = vars[1]
	K = vars[2]
	PSFC = vars[3]
	eta_P = vars[4]
	zeta = vars[5]
	X_h_V = vars[6]
	C_L_1 = vars[7]

	eq = Eq(X_h_V, 2*eta_P*E_max/PSFC*atan((E_1*zeta)/(2*E_max*(1-K*E_1*C_L_1*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Range h_V')
vars_names['Propeller Range h_V'] = ['Initial Efficiency', 'Max Efficiency', 'Induced Drag Factor', 'Power Specific Fuel Consumption', 'Populsive Efficiency', 'Fuel Weight ratio', 'Range h-V', 'Cruise Initial C_L']
variables['Propeller Range h_V'] = ['E_1', 'E_max', 'K', 'PSFC', 'eta_P', 'zeta', 'X_h_V', 'C_L_1']
formulas['Propeller Range h_V'] = 'X_h_V = 2*eta_P*E_max/PSFC*atan((E_1*zeta)/(2*E_max*(1-K*E_1*C_L_1*zeta)))'
num_vars['Propeller Range h_V'] = 8
equations['Propeller Range h_V'] = Propeller_Range_h_V
# 
# 
# 
def Propeller_Range_V_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	PSFC = vars[1]
	eta_P = vars[2]
	zeta = vars[3]
	X_V_C_L = vars[4]

	eq = Eq(X_V_C_L, eta_P*E/PSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Range V_C_L')
vars_names['Propeller Range V_C_L'] = ['Efficiency', 'Power Specific Fuel Consumption', 'Populsive Efficiency', 'Fuel Weight ratio', 'Range V-C_L']
variables['Propeller Range V_C_L'] = ['E', 'PSFC', 'eta_P', 'zeta', 'X_V_C_L']
formulas['Propeller Range V_C_L'] = 'X_V_C_L = eta_P*E/PSFC*ln(1/(1-zeta))'
num_vars['Propeller Range V_C_L'] = 5
equations['Propeller Range V_C_L'] = Propeller_Range_V_C_L
# 
# 
# 
def Propeller_Range_h_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	PSFC = vars[1]
	eta_P = vars[2]
	zeta = vars[3]
	X_h_C_L = vars[4]

	eq = Eq(X_h_C_L, eta_P*E/PSFC*ln(1-(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Range h_C_L')
vars_names['Propeller Range h_C_L'] = ['Efficiency', 'Power Specific Fuel Consumption', 'Populsive Efficiency', 'Fuel Weight ratio', 'Range h-C_L']
variables['Propeller Range h_C_L'] = ['E', 'PSFC', 'eta_P', 'zeta', 'X_h_C_L']
formulas['Propeller Range h_C_L'] = 'X_h_C_L = eta_P*E/PSFC*ln(1-(1-zeta))'
num_vars['Propeller Range h_C_L'] = 5
equations['Propeller Range h_C_L'] = Propeller_Range_h_C_L
# 
# 
# 
def Propeller_Endurance_h_V(solv_vars, vars, dict_val):
	E_1 = vars[0]
	E_max = vars[1]
	K = vars[2]
	PSFC = vars[3]
	V = vars[4]
	eta_P = vars[5]
	t_h_V = vars[6]
	zeta = vars[7]
	C_L_1 = vars[8]

	eq = Eq(t_h_V, 2*eta_P*E_max/(PSFC*V)*atan((E_1*zeta)/(2*E_max*(1-K*E_1*C_L_1*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Endurance h_V')
vars_names['Propeller Endurance h_V'] = ['Initial Efficiency', 'Max Efficiency', 'Induced Drag Factor', 'Power Specific Fuel Consumption', 'Speed', 'Populsive Efficiency', 'Endurance h-V', 'Fuel Weight ratio', 'Cruise Initial C_L']
variables['Propeller Endurance h_V'] = ['E_1', 'E_max', 'K', 'PSFC', 'V', 'eta_P', 't_h_V', 'zeta', 'C_L_1']
formulas['Propeller Endurance h_V'] = 't_h_V = 2*eta_P*E_max/(PSFC*V)*atan((E_1*zeta)/(2*E_max*(1-K*E_1*C_L_1*zeta)))'
num_vars['Propeller Endurance h_V'] = 9
equations['Propeller Endurance h_V'] = Propeller_Endurance_h_V
# 
# 
# 
def Propeller_Endurance_V_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	PSFC = vars[1]
	V = vars[2]
	eta_P = vars[3]
	t_V_C_L = vars[4]
	zeta = vars[5]

	eq = Eq(t_V_C_L, eta_P/PSFC*E/V*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Endurance V_C_L')
vars_names['Propeller Endurance V_C_L'] = ['Efficiency', 'Power Specific Fuel Consumption', 'Speed', 'Populsive Efficiency', 'Endurance V-C_L', 'Fuel Weight ratio']
variables['Propeller Endurance V_C_L'] = ['E', 'PSFC', 'V', 'eta_P', 't_V_C_L', 'zeta']
formulas['Propeller Endurance V_C_L'] = 't_V_C_L = eta_P/PSFC*E/V*ln(1/(1-zeta))'
num_vars['Propeller Endurance V_C_L'] = 6
equations['Propeller Endurance V_C_L'] = Propeller_Endurance_V_C_L
# 
# 
# 
def Propeller_Endurance_h_C_L(solv_vars, vars, dict_val):
	E = vars[0]
	PSFC = vars[1]
	V_1 = vars[2]
	eta_P = vars[3]
	t_h_C_L = vars[4]
	zeta = vars[5]

	eq = Eq(t_h_C_L, 2*eta_P*E/(PSFC*V_1)*(1-sqrt(1-zeta)/sqrt(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Endurance h_C_L')
vars_names['Propeller Endurance h_C_L'] = ['Efficiency', 'Power Specific Fuel Consumption', 'Cruise Initial Speed', 'Populsive Efficiency', 'Endurance h-C_L', 'Fuel Weight ratio']
variables['Propeller Endurance h_C_L'] = ['E', 'PSFC', 'V_1', 'eta_P', 't_h_C_L', 'zeta']
formulas['Propeller Endurance h_C_L'] = 't_h_C_L = 2*eta_P*E/(PSFC*V_1)*(1-sqrt(1-zeta)/sqrt(1-zeta))'
num_vars['Propeller Endurance h_C_L'] = 6
equations['Propeller Endurance h_C_L'] = Propeller_Endurance_h_C_L
# 
# 
# 
def Propeller_Best_Range_Efficiency(solv_vars, vars, dict_val):
	E_max = vars[0]
	E_br = vars[1]

	eq = Eq(E_br, E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Range Efficiency')
vars_names['Propeller Best Range Efficiency'] = ['Max Efficiency', 'Best Range Efficiency']
variables['Propeller Best Range Efficiency'] = ['E_max', 'E_br']
formulas['Propeller Best Range Efficiency'] = 'E_br = E_max'
num_vars['Propeller Best Range Efficiency'] = 2
equations['Propeller Best Range Efficiency'] = Propeller_Best_Range_Efficiency
# 
# 
# 
def Propeller_Best_Range_Speed(solv_vars, vars, dict_val):
	V_D_min = vars[0]
	V_br = vars[1]

	eq = Eq(V_br, V_D_min)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Range Speed')
vars_names['Propeller Best Range Speed'] = ['Min Drag Speed', 'Best Range Speed']
variables['Propeller Best Range Speed'] = ['V_D_min', 'V_br']
formulas['Propeller Best Range Speed'] = 'V_br = V_D_min'
num_vars['Propeller Best Range Speed'] = 2
equations['Propeller Best Range Speed'] = Propeller_Best_Range_Speed
# 
# 
# 
def Propeller_Best_Range_V_C_L(solv_vars, vars, dict_val):
	C_L_E_max = vars[0]
	E_max = vars[1]
	K = vars[2]
	PSFC = vars[3]
	eta_P = vars[4]
	zeta = vars[5]
	X_br_h_V = vars[6]

	eq = Eq(X_br_h_V, 2*eta_P*E_max/PSFC*atan(zeta/(2*(1-K*E_max*C_L_E_max*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Range V_C_L')
vars_names['Propeller Best Range V_C_L'] = ['Max Efficiency C_L', 'Max Efficiency', 'Induced Drag Factor', 'Power Specific Fuel Consumption', 'Populsive Efficiency', 'Fuel Weight ratio', 'Best Range h-V']
variables['Propeller Best Range V_C_L'] = ['C_L_E_max', 'E_max', 'K', 'PSFC', 'eta_P', 'zeta', 'X_br_h_V']
formulas['Propeller Best Range V_C_L'] = 'X_br_h_V = 2*eta_P*E_max/PSFC*atan(zeta/(2*(1-K*E_max*C_L_E_max*zeta)))'
num_vars['Propeller Best Range V_C_L'] = 7
equations['Propeller Best Range V_C_L'] = Propeller_Best_Range_V_C_L
# 
# 
# 
def Propeller_Best_Range_h_V(solv_vars, vars, dict_val):
	E_max = vars[0]
	PSFC = vars[1]
	eta_P = vars[2]
	zeta = vars[3]
	X_br_V_C_L = vars[4]

	eq = Eq(X_br_V_C_L, eta_P*E_max/PSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Range h_V')
vars_names['Propeller Best Range h_V'] = ['Max Efficiency', 'Power Specific Fuel Consumption', 'Populsive Efficiency', 'Fuel Weight ratio', 'Best Range V-C_L']
variables['Propeller Best Range h_V'] = ['E_max', 'PSFC', 'eta_P', 'zeta', 'X_br_V_C_L']
formulas['Propeller Best Range h_V'] = 'X_br_V_C_L = eta_P*E_max/PSFC*ln(1/(1-zeta))'
num_vars['Propeller Best Range h_V'] = 5
equations['Propeller Best Range h_V'] = Propeller_Best_Range_h_V
# 
# 
# 
def Propeller_Best_Range_h_C_L(solv_vars, vars, dict_val):
	E_max = vars[0]
	PSFC = vars[1]
	eta_P = vars[2]
	zeta = vars[3]
	X_br_h_C_L = vars[4]

	eq = Eq(X_br_h_C_L, eta_P*E_max/PSFC*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Range h_C_L')
vars_names['Propeller Best Range h_C_L'] = ['Max Efficiency', 'Power Specific Fuel Consumption', 'Populsive Efficiency', 'Fuel Weight ratio', 'Best Range h-C_L']
variables['Propeller Best Range h_C_L'] = ['E_max', 'PSFC', 'eta_P', 'zeta', 'X_br_h_C_L']
formulas['Propeller Best Range h_C_L'] = 'X_br_h_C_L = eta_P*E_max/PSFC*ln(1/(1-zeta))'
num_vars['Propeller Best Range h_C_L'] = 5
equations['Propeller Best Range h_C_L'] = Propeller_Best_Range_h_C_L
# 
# 
# 
def Propeller_Best_Endurance_Efficiency(solv_vars, vars, dict_val):
	E_P_min = vars[0]
	E_be = vars[1]

	eq = Eq(E_be, E_P_min)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Endurance Efficiency')
vars_names['Propeller Best Endurance Efficiency'] = ['Min Power Efficiency', 'Best Endurance Efficiency']
variables['Propeller Best Endurance Efficiency'] = ['E_P_min', 'E_be']
formulas['Propeller Best Endurance Efficiency'] = 'E_be = E_P_min'
num_vars['Propeller Best Endurance Efficiency'] = 2
equations['Propeller Best Endurance Efficiency'] = Propeller_Best_Endurance_Efficiency
# 
# 
# 
def Propeller_Best_Endurance_Speed(solv_vars, vars, dict_val):
	V_P_min = vars[0]
	V_be = vars[1]

	eq = Eq(V_be, V_P_min)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Endurance Speed')
vars_names['Propeller Best Endurance Speed'] = ['Min Power Speed', 'Best Endurance Speed']
variables['Propeller Best Endurance Speed'] = ['V_P_min', 'V_be']
formulas['Propeller Best Endurance Speed'] = 'V_be = V_P_min'
num_vars['Propeller Best Endurance Speed'] = 2
equations['Propeller Best Endurance Speed'] = Propeller_Best_Endurance_Speed
# 
# 
# 
def Propeller_Best_Endurance_V_C_L(solv_vars, vars, dict_val):
	E_max = vars[0]
	PSFC = vars[1]
	V_be = vars[2]
	eta_P = vars[3]
	t_be_V_C_L = vars[4]
	zeta = vars[5]

	eq = Eq(t_be_V_C_L, eta_P/PSFC*0.866*E_max/V_be*ln(1/(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Endurance V_C_L')
vars_names['Propeller Best Endurance V_C_L'] = ['Max Efficiency', 'Power Specific Fuel Consumption', 'Best Endurance Speed', 'Populsive Efficiency', 'Best Endurance V-C_L', 'Fuel Weight ratio']
variables['Propeller Best Endurance V_C_L'] = ['E_max', 'PSFC', 'V_be', 'eta_P', 't_be_V_C_L', 'zeta']
formulas['Propeller Best Endurance V_C_L'] = 't_be_V_C_L = eta_P/PSFC*0.866*E_max/V_be*ln(1/(1-zeta))'
num_vars['Propeller Best Endurance V_C_L'] = 6
equations['Propeller Best Endurance V_C_L'] = Propeller_Best_Endurance_V_C_L
# 
# 
# 
def Propeller_Best_Endurance_h_V(solv_vars, vars, dict_val):
	C_L_P_min = vars[0]
	E_P_min = vars[1]
	E_max = vars[2]
	K = vars[3]
	PSFC = vars[4]
	V = vars[5]
	eta_P = vars[6]
	t_be_h_V = vars[7]
	zeta = vars[8]

	eq = Eq(t_be_h_V, 2*eta_P*E_max/(PSFC*V)*atan((E_P_min*zeta)/(2*E_max*(1-K*E_P_min*C_L_P_min*zeta))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Endurance h_V')
vars_names['Propeller Best Endurance h_V'] = ['Min Power C_L', 'Min Power Efficiency', 'Max Efficiency', 'Induced Drag Factor', 'Power Specific Fuel Consumption', 'Speed', 'Populsive Efficiency', 'Best Endurance h-V', 'Fuel Weight ratio']
variables['Propeller Best Endurance h_V'] = ['C_L_P_min', 'E_P_min', 'E_max', 'K', 'PSFC', 'V', 'eta_P', 't_be_h_V', 'zeta']
formulas['Propeller Best Endurance h_V'] = 't_be_h_V = 2*eta_P*E_max/(PSFC*V)*atan((E_P_min*zeta)/(2*E_max*(1-K*E_P_min*C_L_P_min*zeta)))'
num_vars['Propeller Best Endurance h_V'] = 9
equations['Propeller Best Endurance h_V'] = Propeller_Best_Endurance_h_V
# 
# 
# 
def Propeller_Best_Endurance_h_C_L(solv_vars, vars, dict_val):
	E_max = vars[0]
	PSFC = vars[1]
	V_be_1 = vars[2]
	eta_P = vars[3]
	t_be_h_C_L = vars[4]
	zeta = vars[5]

	eq = Eq(t_be_h_C_L, 2*eta_P*0.866*E_max/(PSFC*V_be_1)*(1-sqrt(1-zeta)/sqrt(1-zeta)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Best Endurance h_C_L')
vars_names['Propeller Best Endurance h_C_L'] = ['Max Efficiency', 'Power Specific Fuel Consumption', 'Best Endurance Initial Speed', 'Populsive Efficiency', 'Best Endurance h-C_L', 'Fuel Weight ratio']
variables['Propeller Best Endurance h_C_L'] = ['E_max', 'PSFC', 'V_be_1', 'eta_P', 't_be_h_C_L', 'zeta']
formulas['Propeller Best Endurance h_C_L'] = 't_be_h_C_L = 2*eta_P*0.866*E_max/(PSFC*V_be_1)*(1-sqrt(1-zeta)/sqrt(1-zeta))'
num_vars['Propeller Best Endurance h_C_L'] = 6
equations['Propeller Best Endurance h_C_L'] = Propeller_Best_Endurance_h_C_L
# 
# 
# 
