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
def Load_Factor_Looping(solv_vars, vars, dict_val):
	V = vars[0]
	g = vars[1]
	n_loop = vars[2]
	r = vars[3]
	theta = vars[4]

	eq = Eq(n_loop, cos(theta)+(1/g)*V**2/r)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Load Factor Looping')
vars_names['Load Factor Looping'] = ['Speed', 'Gravity Acc', 'Loop Load Factor', 'Radius', 'Turn Angle']
variables['Load Factor Looping'] = ['V', 'g', 'n_loop', 'r', 'theta']
formulas['Load Factor Looping'] = 'n_loop = cos(theta)+(1/g)*V**2/r'
num_vars['Load Factor Looping'] = 5
equations['Load Factor Looping'] = Load_Factor_Looping
# 
# 
# 
def Radius_Looping(solv_vars, vars, dict_val):
	V = vars[0]
	g = vars[1]
	n_theta_90 = vars[2]
	r_loop = vars[3]

	eq = Eq(r_loop, V**2/(g*n_theta_90))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Radius Looping')
vars_names['Radius Looping'] = ['Speed', 'Gravity Acc', 'Load Factor 90º', 'Loop Radius']
variables['Radius Looping'] = ['V', 'g', 'n_theta_90', 'r_loop']
formulas['Radius Looping'] = 'r_loop = V**2/(g*n_theta_90)'
num_vars['Radius Looping'] = 4
equations['Radius Looping'] = Radius_Looping
# 
# 
# 
def Rate_Looping(solv_vars, vars, dict_val):
	V = vars[0]
	omega_loop = vars[1]
	r_loop = vars[2]

	eq = Eq(omega_loop, V/r_loop)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Rate Looping')
vars_names['Rate Looping'] = ['Speed', 'Loop Rate Change', 'Loop Radius']
variables['Rate Looping'] = ['V', 'omega_loop', 'r_loop']
formulas['Rate Looping'] = 'omega_loop = V/r_loop'
num_vars['Rate Looping'] = 3
equations['Rate Looping'] = Rate_Looping
# 
# 
# 
def Lift_Coefficient_Looping(solv_vars, vars, dict_val):
	C_L_loop = vars[0]
	S = vars[1]
	W = vars[2]
	g = vars[3]
	n_theta_90 = vars[4]
	r = vars[5]
	rho = vars[6]
	theta = vars[7]

	eq = Eq(C_L_loop, (2*(n_theta_90-cos(theta))*(W/S))/(g*n_theta_90*rho*r))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Lift Coefficient Looping')
vars_names['Lift Coefficient Looping'] = ['C_L Looping', 'Area', 'Weight', 'Gravity Acc', 'Load Factor 90º', 'Radius', 'Air Density', 'Turn Angle']
variables['Lift Coefficient Looping'] = ['C_L_loop', 'S', 'W', 'g', 'n_theta_90', 'r', 'rho', 'theta']
formulas['Lift Coefficient Looping'] = 'C_L_loop = (2*(n_theta_90-cos(theta))*(W/S))/(g*n_theta_90*rho*r)'
num_vars['Lift Coefficient Looping'] = 8
equations['Lift Coefficient Looping'] = Lift_Coefficient_Looping
# 
# 
# 
