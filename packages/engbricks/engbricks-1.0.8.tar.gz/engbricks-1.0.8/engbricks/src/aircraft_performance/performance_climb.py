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
def Horizontal_Speed(solv_vars, vars, dict_val):
	V = vars[0]
	V_H = vars[1]
	gamma = vars[2]

	eq = Eq(V_H, V*cos(gamma))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Horizontal Speed')
vars_names['Horizontal Speed'] = ['Speed', 'Horizontal Speed', 'Climb Angle']
variables['Horizontal Speed'] = ['V', 'V_H', 'gamma']
formulas['Horizontal Speed'] = 'V_H = V*cos(gamma)'
num_vars['Horizontal Speed'] = 3
equations['Horizontal Speed'] = Horizontal_Speed
# 
# 
# 
def Jet_Climb_Rate(solv_vars, vars, dict_val):
	RC = vars[0]
	V_V = vars[1]

	eq = Eq(V_V, RC)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Climb Rate')
vars_names['Jet Climb Rate'] = ['Rate of Climb', 'Vertical Speed']
variables['Jet Climb Rate'] = ['RC', 'V_V']
formulas['Jet Climb Rate'] = 'V_V = RC'
num_vars['Jet Climb Rate'] = 2
equations['Jet Climb Rate'] = Jet_Climb_Rate
# 
# 
# 
def Jet_Climb_Angle(solv_vars, vars, dict_val):
	D = vars[0]
	RC = vars[1]
	T = vars[2]
	V = vars[3]
	W = vars[4]

	eq = Eq(RC, (T*V-D*V)/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Climb Angle')
vars_names['Jet Climb Angle'] = ['Drag', 'Rate of Climb', 'Thrust', 'Speed', 'Weight']
variables['Jet Climb Angle'] = ['D', 'RC', 'T', 'V', 'W']
formulas['Jet Climb Angle'] = 'RC = (T*V-D*V)/W'
num_vars['Jet Climb Angle'] = 5
equations['Jet Climb Angle'] = Jet_Climb_Angle
# 
# 
# 
def Jet_Maximum_Climb_Angle(solv_vars, vars, dict_val):
	D = vars[0]
	T = vars[1]
	W = vars[2]
	gamma = vars[3]

	eq = Eq(sin(gamma), (T-D)/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Maximum Climb Angle')
vars_names['Jet Maximum Climb Angle'] = ['Drag', 'Thrust', 'Weight', 'Climb Angle']
variables['Jet Maximum Climb Angle'] = ['D', 'T', 'W', 'gamma']
formulas['Jet Maximum Climb Angle'] = 'sin(gamma) = (T-D)/W'
num_vars['Jet Maximum Climb Angle'] = 4
equations['Jet Maximum Climb Angle'] = Jet_Maximum_Climb_Angle
# 
# 
# 
def Jet_Speed_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	E_max = vars[0]
	T = vars[1]
	W = vars[2]
	gamma_max = vars[3]

	eq = Eq(sin(gamma_max), T/W-1/E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Speed Maximum Climb Rate')
vars_names['Jet Speed Maximum Climb Rate'] = ['Max Efficiency', 'Thrust', 'Weight', 'Max Climb angle']
variables['Jet Speed Maximum Climb Rate'] = ['E_max', 'T', 'W', 'gamma_max']
formulas['Jet Speed Maximum Climb Rate'] = 'sin(gamma_max) = T/W-1/E_max'
num_vars['Jet Speed Maximum Climb Rate'] = 4
equations['Jet Speed Maximum Climb Rate'] = Jet_Speed_Maximum_Climb_Rate
# 
# 
# 
def Jet_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	E_max = vars[1]
	S = vars[2]
	T = vars[3]
	V_RC_max = vars[4]
	W = vars[5]
	rho = vars[6]

	eq = Eq(V_RC_max, sqrt((T/S)/(3*rho*C_D0)*(1+sqrt(1+3/(E_max*T/W)**2))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Maximum Climb Rate')
vars_names['Jet Maximum Climb Rate'] = ['Parasite Drag Coefficient', 'Max Efficiency', 'Area', 'Thrust', 'Speed Max RC', 'Weight', 'Air Density']
variables['Jet Maximum Climb Rate'] = ['C_D0', 'E_max', 'S', 'T', 'V_RC_max', 'W', 'rho']
formulas['Jet Maximum Climb Rate'] = 'V_RC_max = sqrt((T/S)/(3*rho*C_D0)*(1+sqrt(1+3/(E_max*T/W)**2)))'
num_vars['Jet Maximum Climb Rate'] = 7
equations['Jet Maximum Climb Rate'] = Jet_Maximum_Climb_Rate
# 
# 
# 
def Jet_Drag_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	D_RC_max = vars[0]
	RC_max = vars[1]
	T = vars[2]
	V_RC_max = vars[3]
	W = vars[4]

	eq = Eq(RC_max, (T*V_RC_max-D_RC_max*V_RC_max)/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Drag Maximum Climb Rate')
vars_names['Jet Drag Maximum Climb Rate'] = ['Max RC Drag', 'Max RC', 'Thrust', 'Speed Max RC', 'Weight']
variables['Jet Drag Maximum Climb Rate'] = ['D_RC_max', 'RC_max', 'T', 'V_RC_max', 'W']
formulas['Jet Drag Maximum Climb Rate'] = 'RC_max = (T*V_RC_max-D_RC_max*V_RC_max)/W'
num_vars['Jet Drag Maximum Climb Rate'] = 5
equations['Jet Drag Maximum Climb Rate'] = Jet_Drag_Maximum_Climb_Rate
# 
# 
# 
def Jet_Angle_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	D_RC_max = vars[1]
	K = vars[2]
	S = vars[3]
	V_RC_max = vars[4]
	W = vars[5]
	gamma = vars[6]
	rho = vars[7]

	eq = Eq(D_RC_max, 1/2*rho*V_RC_max*S*C_D0+(K*W**2*cos**(gamma))/(0.5*rho*V_RC_max*S))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Angle Maximum Climb Rate')
vars_names['Jet Angle Maximum Climb Rate'] = ['Parasite Drag Coefficient', 'Max RC Drag', 'Induced Drag Factor', 'Area', 'Speed Max RC', 'Weight', 'Climb Angle', 'Air Density']
variables['Jet Angle Maximum Climb Rate'] = ['C_D0', 'D_RC_max', 'K', 'S', 'V_RC_max', 'W', 'gamma', 'rho']
formulas['Jet Angle Maximum Climb Rate'] = 'D_RC_max = 1/2*rho*V_RC_max*S*C_D0+(K*W**2*cos**(gamma))/(0.5*rho*V_RC_max*S)'
num_vars['Jet Angle Maximum Climb Rate'] = 8
equations['Jet Angle Maximum Climb Rate'] = Jet_Angle_Maximum_Climb_Rate
# 
# 
# 
def Propeller_Climb_Rate(solv_vars, vars, dict_val):
	RC_max = vars[0]
	V_RC_max = vars[1]
	gamma_RC_max = vars[2]

	eq = Eq(sin(gamma_RC_max), RC_max/V_RC_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Climb Rate')
vars_names['Propeller Climb Rate'] = ['Max RC', 'Speed Max RC', 'Max RC Climb Angle']
variables['Propeller Climb Rate'] = ['RC_max', 'V_RC_max', 'gamma_RC_max']
formulas['Propeller Climb Rate'] = 'sin(gamma_RC_max) = RC_max/V_RC_max'
num_vars['Propeller Climb Rate'] = 3
equations['Propeller Climb Rate'] = Propeller_Climb_Rate
# 
# 
# 
def Propeller_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	P_R = vars[0]
	P_e = vars[1]
	RC = vars[2]
	W = vars[3]
	eta_P = vars[4]

	eq = Eq(RC, (eta_P*P_e-P_R)/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Maximum Climb Rate')
vars_names['Propeller Maximum Climb Rate'] = ['Required Power', 'Power effective', 'Rate of Climb', 'Weight', 'Populsive Efficiency']
variables['Propeller Maximum Climb Rate'] = ['P_R', 'P_e', 'RC', 'W', 'eta_P']
formulas['Propeller Maximum Climb Rate'] = 'RC = (eta_P*P_e-P_R)/W'
num_vars['Propeller Maximum Climb Rate'] = 5
equations['Propeller Maximum Climb Rate'] = Propeller_Maximum_Climb_Rate
# 
# 
# 
def Propeller_Speed_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	P_R_min = vars[0]
	P_e = vars[1]
	RC_max = vars[2]
	W = vars[3]
	eta_P = vars[4]

	eq = Eq(RC_max, (eta_P*P_e-P_R_min)/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Speed Maximum Climb Rate')
vars_names['Propeller Speed Maximum Climb Rate'] = ['Min Required Power', 'Power effective', 'Max RC', 'Weight', 'Populsive Efficiency']
variables['Propeller Speed Maximum Climb Rate'] = ['P_R_min', 'P_e', 'RC_max', 'W', 'eta_P']
formulas['Propeller Speed Maximum Climb Rate'] = 'RC_max = (eta_P*P_e-P_R_min)/W'
num_vars['Propeller Speed Maximum Climb Rate'] = 5
equations['Propeller Speed Maximum Climb Rate'] = Propeller_Speed_Maximum_Climb_Rate
# 
# 
# 
def Propeller_Angle_Maximum_Climb_Rate(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_RC_max = vars[3]
	W = vars[4]
	rho = vars[5]

	eq = Eq(V_RC_max, sqrt(W/(0.5*rho*S))*(K/(3*C_D0))**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Angle Maximum Climb Rate')
vars_names['Propeller Angle Maximum Climb Rate'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Speed Max RC', 'Weight', 'Air Density']
variables['Propeller Angle Maximum Climb Rate'] = ['C_D0', 'K', 'S', 'V_RC_max', 'W', 'rho']
formulas['Propeller Angle Maximum Climb Rate'] = 'V_RC_max = sqrt(W/(0.5*rho*S))*(K/(3*C_D0))**1/4'
num_vars['Propeller Angle Maximum Climb Rate'] = 6
equations['Propeller Angle Maximum Climb Rate'] = Propeller_Angle_Maximum_Climb_Rate
# 
# 
# 
def Climb_Time(solv_vars, vars, dict_val):
	RC_max = vars[0]
	V_RC_max = vars[1]
	gamma_RC_max = vars[2]

	eq = Eq(sin(gamma_RC_max), RC_max/V_RC_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Climb Time')
vars_names['Climb Time'] = ['Max RC', 'Speed Max RC', 'Max RC Climb Angle']
variables['Climb Time'] = ['RC_max', 'V_RC_max', 'gamma_RC_max']
formulas['Climb Time'] = 'sin(gamma_RC_max) = RC_max/V_RC_max'
num_vars['Climb Time'] = 3
equations['Climb Time'] = Climb_Time
# 
# 
# 
