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
def Glide_Angle(solv_vars, vars, dict_val):
	D = vars[0]
	W = vars[1]
	gamma = vars[2]

	eq = Eq(sin(gamma), -D/W)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Glide Angle')
vars_names['Glide Angle'] = ['Drag', 'Weight', 'Climb Angle']
variables['Glide Angle'] = ['D', 'W', 'gamma']
formulas['Glide Angle'] = 'sin(gamma) = -D/W'
num_vars['Glide Angle'] = 3
equations['Glide Angle'] = Glide_Angle
# 
# 
# 
def Minimum_Glide_Angle(solv_vars, vars, dict_val):
	E_max = vars[0]
	gamma_min = vars[1]

	eq = Eq(tan(gamma_min), -1/E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Minimum Glide Angle')
vars_names['Minimum Glide Angle'] = ['Max Efficiency', 'Min Glide angle']
variables['Minimum Glide Angle'] = ['E_max', 'gamma_min']
formulas['Minimum Glide Angle'] = 'tan(gamma_min) = -1/E_max'
num_vars['Minimum Glide Angle'] = 2
equations['Minimum Glide Angle'] = Minimum_Glide_Angle
# 
# 
# 
def Speed_Minimum_Glide_Angle(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_gamma_min = vars[3]
	W = vars[4]
	gamma = vars[5]
	rho = vars[6]

	eq = Eq(V_gamma_min, sqrt((W*cos(gamma))/(0.5*rho*S))*(K/(C_D0))**1/4)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed Minimum Glide Angle')
vars_names['Speed Minimum Glide Angle'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Speed Minimum Glide Angle', 'Weight', 'Climb Angle', 'Air Density']
variables['Speed Minimum Glide Angle'] = ['C_D0', 'K', 'S', 'V_gamma_min', 'W', 'gamma', 'rho']
formulas['Speed Minimum Glide Angle'] = 'V_gamma_min = sqrt((W*cos(gamma))/(0.5*rho*S))*(K/(C_D0))**1/4'
num_vars['Speed Minimum Glide Angle'] = 7
equations['Speed Minimum Glide Angle'] = Speed_Minimum_Glide_Angle
# 
# 
# 
def Glide_Range(solv_vars, vars, dict_val):
	E = vars[0]
	X_glide = vars[1]
	h1 = vars[2]
	h2 = vars[3]

	eq = Eq(X_glide, -E*(h2-h1))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Glide Range')
vars_names['Glide Range'] = ['Efficiency', 'Glide Range', 'Initial Altitude', 'Final Altitude']
variables['Glide Range'] = ['E', 'X_glide', 'h1', 'h2']
formulas['Glide Range'] = 'X_glide = -E*(h2-h1)'
num_vars['Glide Range'] = 4
equations['Glide Range'] = Glide_Range
# 
# 
# 
def Glide_Maximum_Range(solv_vars, vars, dict_val):
	E_max = vars[0]
	X_glide_br = vars[1]
	h1 = vars[2]
	h2 = vars[3]

	eq = Eq(X_glide_br, -E_max*(h2-h1))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Glide Maximum Range')
vars_names['Glide Maximum Range'] = ['Max Efficiency', 'Glide Best Range', 'Initial Altitude', 'Final Altitude']
variables['Glide Maximum Range'] = ['E_max', 'X_glide_br', 'h1', 'h2']
formulas['Glide Maximum Range'] = 'X_glide_br = -E_max*(h2-h1)'
num_vars['Glide Maximum Range'] = 4
equations['Glide Maximum Range'] = Glide_Maximum_Range
# 
# 
# 
def Glide_Rate_Of_Descend(solv_vars, vars, dict_val):
	E = vars[0]
	RD_glide = vars[1]
	V = vars[2]

	eq = Eq(RD_glide, V/E)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Glide Rate Of Descend')
vars_names['Glide Rate Of Descend'] = ['Efficiency', 'Glide RD', 'Speed']
variables['Glide Rate Of Descend'] = ['E', 'RD_glide', 'V']
formulas['Glide Rate Of Descend'] = 'RD_glide = V/E'
num_vars['Glide Rate Of Descend'] = 3
equations['Glide Rate Of Descend'] = Glide_Rate_Of_Descend
# 
# 
# 
def Glide_Minimum_Rate_Of_Descend(solv_vars, vars, dict_val):
	E_P_min = vars[0]
	RD_glide_min = vars[1]
	V_P_min = vars[2]

	eq = Eq(RD_glide_min, V_P_min/E_P_min)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Glide Minimum Rate Of Descend')
vars_names['Glide Minimum Rate Of Descend'] = ['Min Power Efficiency', 'Glide Min RD', 'Min Power Speed']
variables['Glide Minimum Rate Of Descend'] = ['E_P_min', 'RD_glide_min', 'V_P_min']
formulas['Glide Minimum Rate Of Descend'] = 'RD_glide_min = V_P_min/E_P_min'
num_vars['Glide Minimum Rate Of Descend'] = 3
equations['Glide Minimum Rate Of Descend'] = Glide_Minimum_Rate_Of_Descend
# 
# 
# 
