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
def Efficiency(solv_vars, vars, dict_val):
	C_D = vars[0]
	C_L = vars[1]
	E = vars[2]

	eq = Eq(E, C_L/C_D)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Efficiency')
vars_names['Efficiency'] = ['Drag Coefficient', 'Lift Coefficient', 'Efficiency']
variables['Efficiency'] = ['C_D', 'C_L', 'E']
formulas['Efficiency'] = 'E = C_L/C_D'
num_vars['Efficiency'] = 3
equations['Efficiency'] = Efficiency
# 
# 
# 
def Maximum_Efficiency(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_max = vars[1]
	K = vars[2]

	eq = Eq(E_max, 1/(2*sqrt(K*C_D0)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Maximum Efficiency')
vars_names['Maximum Efficiency'] = ['Parasite Drag Coefficient', 'Max Efficiency', 'Induced Drag Factor']
variables['Maximum Efficiency'] = ['C_D0', 'E_max', 'K']
formulas['Maximum Efficiency'] = 'E_max = 1/(2*sqrt(K*C_D0))'
num_vars['Maximum Efficiency'] = 3
equations['Maximum Efficiency'] = Maximum_Efficiency
# 
# 
# 
def C_L_At_Maximum_Efficiency(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	C_L_E_max = vars[1]
	K = vars[2]

	eq = Eq(C_L_E_max, sqrt(C_D0/K))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_L At Maximum Efficiency')
vars_names['C_L At Maximum Efficiency'] = ['Parasite Drag Coefficient', 'Max Efficiency C_L', 'Induced Drag Factor']
variables['C_L At Maximum Efficiency'] = ['C_D0', 'C_L_E_max', 'K']
formulas['C_L At Maximum Efficiency'] = 'C_L_E_max = sqrt(C_D0/K)'
num_vars['C_L At Maximum Efficiency'] = 3
equations['C_L At Maximum Efficiency'] = C_L_At_Maximum_Efficiency
# 
# 
# 
def C_D_At_Maximum_Efficiency(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	C_D_E_max = vars[1]

	eq = Eq(C_D_E_max, 2*C_D0)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_D At Maximum Efficiency')
vars_names['C_D At Maximum Efficiency'] = ['Parasite Drag Coefficient', 'Max Efficiency C_D']
variables['C_D At Maximum Efficiency'] = ['C_D0', 'C_D_E_max']
formulas['C_D At Maximum Efficiency'] = 'C_D_E_max = 2*C_D0'
num_vars['C_D At Maximum Efficiency'] = 2
equations['C_D At Maximum Efficiency'] = C_D_At_Maximum_Efficiency
# 
# 
# 
def Speed_At_Maximum_Efficiency(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_E_max = vars[3]
	W = vars[4]
	rho = vars[5]

	eq = Eq(V_E_max, sqrt(2*W/(rho*S))*(K/C_D0)**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed At Maximum Efficiency')
vars_names['Speed At Maximum Efficiency'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Max Efficiency Speed', 'Weight', 'Air Density']
variables['Speed At Maximum Efficiency'] = ['C_D0', 'K', 'S', 'V_E_max', 'W', 'rho']
formulas['Speed At Maximum Efficiency'] = 'V_E_max = sqrt(2*W/(rho*S))*(K/C_D0)**1/4'
num_vars['Speed At Maximum Efficiency'] = 6
equations['Speed At Maximum Efficiency'] = Speed_At_Maximum_Efficiency
# 
# 
# 
def Power_At_Maximum_Efficiency(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_max = vars[1]
	K = vars[2]
	P_E_max = vars[3]
	S = vars[4]
	W = vars[5]
	rho = vars[6]

	eq = Eq(P_E_max, W/E_max*sqrt(2*W/(rho*S))*(K/C_D0)**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Power At Maximum Efficiency')
vars_names['Power At Maximum Efficiency'] = ['Parasite Drag Coefficient', 'Max Efficiency', 'Induced Drag Factor', 'Max Efficiency Power', 'Area', 'Weight', 'Air Density']
variables['Power At Maximum Efficiency'] = ['C_D0', 'E_max', 'K', 'P_E_max', 'S', 'W', 'rho']
formulas['Power At Maximum Efficiency'] = 'P_E_max = W/E_max*sqrt(2*W/(rho*S))*(K/C_D0)**1/4'
num_vars['Power At Maximum Efficiency'] = 7
equations['Power At Maximum Efficiency'] = Power_At_Maximum_Efficiency
# 
# 
# 
def Lower_Speed_(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_max = vars[1]
	S = vars[2]
	T_R = vars[3]
	V_lower = vars[4]
	W = vars[5]
	rho = vars[6]

	eq = Eq(V_lower, (T_R/(S*rho*C_D0)*(1-sqrt(1-1/(E_max*T_R/W)**2)))**(1/2))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Lower Speed ')
vars_names['Lower Speed '] = ['Parasite Drag Coefficient', 'Max Efficiency', 'Area', 'Required Thrust', 'Lower Speed', 'Weight', 'Air Density']
variables['Lower Speed '] = ['C_D0', 'E_max', 'S', 'T_R', 'V_lower', 'W', 'rho']
formulas['Lower Speed '] = 'V_lower = (T_R/(S*rho*C_D0)*(1-sqrt(1-1/(E_max*T_R/W)**2)))**(1/2)'
num_vars['Lower Speed '] = 7
equations['Lower Speed '] = Lower_Speed_
# 
# 
# 
def Higher_Speed(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_max = vars[1]
	S = vars[2]
	T_R = vars[3]
	V_higher = vars[4]
	W = vars[5]
	rho = vars[6]

	eq = Eq(V_higher, (T_R/(S*rho*C_D0)*(1+sqrt(1-1/(E_max*T_R/W)**2)))**(1/2))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Higher Speed')
vars_names['Higher Speed'] = ['Parasite Drag Coefficient', 'Max Efficiency', 'Area', 'Required Thrust', 'Higher Speed', 'Weight', 'Air Density']
variables['Higher Speed'] = ['C_D0', 'E_max', 'S', 'T_R', 'V_higher', 'W', 'rho']
formulas['Higher Speed'] = 'V_higher = (T_R/(S*rho*C_D0)*(1+sqrt(1-1/(E_max*T_R/W)**2)))**(1/2)'
num_vars['Higher Speed'] = 7
equations['Higher Speed'] = Higher_Speed
# 
# 
# 
def Efficiency_At_Tangent_Point_C_D_vs_V(solv_vars, vars, dict_val):
	E_max = vars[0]
	E_tg = vars[1]

	eq = Eq(E_tg, sqrt(3)/2*E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Efficiency At Tangent Point (C_D vs V)')
vars_names['Efficiency At Tangent Point (C_D vs V)'] = ['Max Efficiency', 'Tangent Efficiency']
variables['Efficiency At Tangent Point (C_D vs V)'] = ['E_max', 'E_tg']
formulas['Efficiency At Tangent Point (C_D vs V)'] = 'E_tg = sqrt(3)/2*E_max'
num_vars['Efficiency At Tangent Point (C_D vs V)'] = 2
equations['Efficiency At Tangent Point (C_D vs V)'] = Efficiency_At_Tangent_Point_C_D_vs_V
# 
# 
# 
def C_L_At_Tangent_Point_C_D_vs_V(solv_vars, vars, dict_val):
	C_L_E_max = vars[0]
	C_L_tg = vars[1]

	eq = Eq(C_L_tg, 1/sqrt(3)*C_L_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_L At Tangent Point (C_D vs V)')
vars_names['C_L At Tangent Point (C_D vs V)'] = ['Max Efficiency C_L', 'Tangent C_L']
variables['C_L At Tangent Point (C_D vs V)'] = ['C_L_E_max', 'C_L_tg']
formulas['C_L At Tangent Point (C_D vs V)'] = 'C_L_tg = 1/sqrt(3)*C_L_E_max'
num_vars['C_L At Tangent Point (C_D vs V)'] = 2
equations['C_L At Tangent Point (C_D vs V)'] = C_L_At_Tangent_Point_C_D_vs_V
# 
# 
# 
def C_D_At_Tangent_Point_C_D_vs_V(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	C_D_tg = vars[1]

	eq = Eq(C_D_tg, 4/3*C_D0)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_D At Tangent Point (C_D vs V)')
vars_names['C_D At Tangent Point (C_D vs V)'] = ['Parasite Drag Coefficient', 'Tangent C_D']
variables['C_D At Tangent Point (C_D vs V)'] = ['C_D0', 'C_D_tg']
formulas['C_D At Tangent Point (C_D vs V)'] = 'C_D_tg = 4/3*C_D0'
num_vars['C_D At Tangent Point (C_D vs V)'] = 2
equations['C_D At Tangent Point (C_D vs V)'] = C_D_At_Tangent_Point_C_D_vs_V
# 
# 
# 
def Speed_At_Tangent_Point_C_D_vs_V(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_tg = vars[3]
	W = vars[4]
	rho = vars[5]

	eq = Eq(V_tg, sqrt(2*W/(rho*S))*(3*K/C_D0)**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed At Tangent Point (C_D vs V)')
vars_names['Speed At Tangent Point (C_D vs V)'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Tangent Speed', 'Weight', 'Air Density']
variables['Speed At Tangent Point (C_D vs V)'] = ['C_D0', 'K', 'S', 'V_tg', 'W', 'rho']
formulas['Speed At Tangent Point (C_D vs V)'] = 'V_tg = sqrt(2*W/(rho*S))*(3*K/C_D0)**1/4'
num_vars['Speed At Tangent Point (C_D vs V)'] = 6
equations['Speed At Tangent Point (C_D vs V)'] = Speed_At_Tangent_Point_C_D_vs_V
# 
# 
# 
def Speed_At_Minimum_Drag(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_D_min = vars[3]
	W = vars[4]
	rho_0 = vars[5]
	sigma = vars[6]

	eq = Eq(V_D_min, sqrt(2/(rho_0*sigma)*W/S)*(K/C_D0)**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed At Minimum Drag')
vars_names['Speed At Minimum Drag'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Min Drag Speed', 'Weight', 'Air Density Sea Level', 'sigma']
variables['Speed At Minimum Drag'] = ['C_D0', 'K', 'S', 'V_D_min', 'W', 'rho_0', 'sigma']
formulas['Speed At Minimum Drag'] = 'V_D_min = sqrt(2/(rho_0*sigma)*W/S)*(K/C_D0)**1/4'
num_vars['Speed At Minimum Drag'] = 7
equations['Speed At Minimum Drag'] = Speed_At_Minimum_Drag
# 
# 
# 
def Required_Thrust(solv_vars, vars, dict_val):
	D = vars[0]
	T_R = vars[1]

	eq = Eq(T_R, D)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Required Thrust')
vars_names['Required Thrust'] = ['Drag', 'Required Thrust']
variables['Required Thrust'] = ['D', 'T_R']
formulas['Required Thrust'] = 'T_R = D'
num_vars['Required Thrust'] = 2
equations['Required Thrust'] = Required_Thrust
# 
# 
# 
def Required_Power(solv_vars, vars, dict_val):
	P_R = vars[0]
	T_R = vars[1]
	V = vars[2]

	eq = Eq(P_R, T_R*V)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Required Power')
vars_names['Required Power'] = ['Required Power', 'Required Thrust', 'Speed']
variables['Required Power'] = ['P_R', 'T_R', 'V']
formulas['Required Power'] = 'P_R = T_R*V'
num_vars['Required Power'] = 3
equations['Required Power'] = Required_Power
# 
# 
# 
def Minimum_Power(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_P_min = vars[1]
	K = vars[2]
	P_min = vars[3]
	S = vars[4]
	W = vars[5]
	rho = vars[6]

	eq = Eq(P_min, W/E_P_min*sqrt((2*W)/(rho*S))(K/(3*C_D0))**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Minimum Power')
vars_names['Minimum Power'] = ['Parasite Drag Coefficient', 'Min Power Efficiency', 'Induced Drag Factor', 'Min Power', 'Area', 'Weight', 'Air Density']
variables['Minimum Power'] = ['C_D0', 'E_P_min', 'K', 'P_min', 'S', 'W', 'rho']
formulas['Minimum Power'] = 'P_min = W/E_P_min*sqrt((2*W)/(rho*S))(K/(3*C_D0))**1/4'
num_vars['Minimum Power'] = 7
equations['Minimum Power'] = Minimum_Power
# 
# 
# 
def Efficiency_At_Minimum_Power(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_P_min = vars[1]
	K = vars[2]

	eq = Eq(E_P_min, sqrt(3/(16*K*C_D0)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Efficiency At Minimum Power')
vars_names['Efficiency At Minimum Power'] = ['Parasite Drag Coefficient', 'Min Power Efficiency', 'Induced Drag Factor']
variables['Efficiency At Minimum Power'] = ['C_D0', 'E_P_min', 'K']
formulas['Efficiency At Minimum Power'] = 'E_P_min = sqrt(3/(16*K*C_D0))'
num_vars['Efficiency At Minimum Power'] = 3
equations['Efficiency At Minimum Power'] = Efficiency_At_Minimum_Power
# 
# 
# 
def C_D_At_Minimum_Power(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	C_D_P_min = vars[1]

	eq = Eq(C_D_P_min, 4*C_D0)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_D At Minimum Power')
vars_names['C_D At Minimum Power'] = ['Parasite Drag Coefficient', 'Min Power C_D']
variables['C_D At Minimum Power'] = ['C_D0', 'C_D_P_min']
formulas['C_D At Minimum Power'] = 'C_D_P_min = 4*C_D0'
num_vars['C_D At Minimum Power'] = 2
equations['C_D At Minimum Power'] = C_D_At_Minimum_Power
# 
# 
# 
def C_L_At_Minimum_Power(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	C_L_P_min = vars[1]
	K = vars[2]

	eq = Eq(C_L_P_min, sqrt(3*C_D0/K))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_L At Minimum Power')
vars_names['C_L At Minimum Power'] = ['Parasite Drag Coefficient', 'Min Power C_L', 'Induced Drag Factor']
variables['C_L At Minimum Power'] = ['C_D0', 'C_L_P_min', 'K']
formulas['C_L At Minimum Power'] = 'C_L_P_min = sqrt(3*C_D0/K)'
num_vars['C_L At Minimum Power'] = 3
equations['C_L At Minimum Power'] = C_L_At_Minimum_Power
# 
# 
# 
def Speed_At_Minimum_Power(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_P_min = vars[3]
	W = vars[4]
	rho = vars[5]

	eq = Eq(V_P_min, sqrt(2/rho*W/S)*(K/(3*C_D0))**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed At Minimum Power')
vars_names['Speed At Minimum Power'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Min Power Speed', 'Weight', 'Air Density']
variables['Speed At Minimum Power'] = ['C_D0', 'K', 'S', 'V_P_min', 'W', 'rho']
formulas['Speed At Minimum Power'] = 'V_P_min = sqrt(2/rho*W/S)*(K/(3*C_D0))**1/4'
num_vars['Speed At Minimum Power'] = 6
equations['Speed At Minimum Power'] = Speed_At_Minimum_Power
# 
# 
# 
def Efficiency_At_Tangent_Point_P_R_vs_V(solv_vars, vars, dict_val):
	E_max = vars[0]
	E_tg = vars[1]

	eq = Eq(E_tg, E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Efficiency At Tangent Point (P_R vs V)')
vars_names['Efficiency At Tangent Point (P_R vs V)'] = ['Max Efficiency', 'Tangent Efficiency']
variables['Efficiency At Tangent Point (P_R vs V)'] = ['E_max', 'E_tg']
formulas['Efficiency At Tangent Point (P_R vs V)'] = 'E_tg = E_max'
num_vars['Efficiency At Tangent Point (P_R vs V)'] = 2
equations['Efficiency At Tangent Point (P_R vs V)'] = Efficiency_At_Tangent_Point_P_R_vs_V
# 
# 
# 
def C_L_At_Tangent_Point_P_R_vs_V(solv_vars, vars, dict_val):
	C_L_E_max = vars[0]
	C_L_E_tg = vars[1]

	eq = Eq(C_L_E_tg, C_L_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_L At Tangent Point (P_R vs V)')
vars_names['C_L At Tangent Point (P_R vs V)'] = ['Max Efficiency C_L', 'Tan Efficiency C_L']
variables['C_L At Tangent Point (P_R vs V)'] = ['C_L_E_max', 'C_L_E_tg']
formulas['C_L At Tangent Point (P_R vs V)'] = 'C_L_E_tg = C_L_E_max'
num_vars['C_L At Tangent Point (P_R vs V)'] = 2
equations['C_L At Tangent Point (P_R vs V)'] = C_L_At_Tangent_Point_P_R_vs_V
# 
# 
# 
def C_D_At_Tangent_Point_P_R_vs_V(solv_vars, vars, dict_val):
	C_D_E_max = vars[0]
	C_D_E_tg = vars[1]

	eq = Eq(C_D_E_tg, C_D_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('C_D At Tangent Point (P_R vs V)')
vars_names['C_D At Tangent Point (P_R vs V)'] = ['Max Efficiency C_D', 'Tangent Efficiency C_D']
variables['C_D At Tangent Point (P_R vs V)'] = ['C_D_E_max', 'C_D_E_tg']
formulas['C_D At Tangent Point (P_R vs V)'] = 'C_D_E_tg = C_D_E_max'
num_vars['C_D At Tangent Point (P_R vs V)'] = 2
equations['C_D At Tangent Point (P_R vs V)'] = C_D_At_Tangent_Point_P_R_vs_V
# 
# 
# 
def Speed_At_Tangent_Point_P_R_vs_V(solv_vars, vars, dict_val):
	V_E_max = vars[0]
	V_tg = vars[1]

	eq = Eq(V_tg, V_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed At Tangent Point (P_R vs V)')
vars_names['Speed At Tangent Point (P_R vs V)'] = ['Max Efficiency Speed', 'Tangent Speed']
variables['Speed At Tangent Point (P_R vs V)'] = ['V_E_max', 'V_tg']
formulas['Speed At Tangent Point (P_R vs V)'] = 'V_tg = V_E_max'
num_vars['Speed At Tangent Point (P_R vs V)'] = 2
equations['Speed At Tangent Point (P_R vs V)'] = Speed_At_Tangent_Point_P_R_vs_V
# 
# 
# 
def Power_At_Tangent_Point_P_R_vs_V(solv_vars, vars, dict_val):
	P_E_max = vars[0]
	P_tg = vars[1]

	eq = Eq(P_tg, P_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Power At Tangent Point (P_R vs V)')
vars_names['Power At Tangent Point (P_R vs V)'] = ['Max Efficiency Power', 'Tangent Power']
variables['Power At Tangent Point (P_R vs V)'] = ['P_E_max', 'P_tg']
formulas['Power At Tangent Point (P_R vs V)'] = 'P_tg = P_E_max'
num_vars['Power At Tangent Point (P_R vs V)'] = 2
equations['Power At Tangent Point (P_R vs V)'] = Power_At_Tangent_Point_P_R_vs_V
# 
# 
# 
