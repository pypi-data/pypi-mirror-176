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
def Aspect_Ratio(solv_vars, vars, dict_val):
	Ar = vars[0]
	S = vars[1]
	b = vars[2]

	eq = Eq(Ar, b**2/S)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Aspect Ratio')
vars_names['Aspect Ratio'] = ['Aspect Ratio', 'Area', 'Span']
variables['Aspect Ratio'] = ['Ar', 'S', 'b']
formulas['Aspect Ratio'] = 'Ar = b**2/S'
num_vars['Aspect Ratio'] = 3
equations['Aspect Ratio'] = Aspect_Ratio
# 
# 
# 
def Taper_Ratio(solv_vars, vars, dict_val):
	c_r = vars[0]
	c_t = vars[1]
	lambda_ = vars[2]

	eq = Eq(lambda_, c_t/c_r)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Taper Ratio')
vars_names['Taper Ratio'] = ['Root Chord', 'Tip Chord', 'Taper Ratio']
variables['Taper Ratio'] = ['c_r', 'c_t', 'lambda_']
formulas['Taper Ratio'] = 'lambda_ = c_t/c_r'
num_vars['Taper Ratio'] = 3
equations['Taper Ratio'] = Taper_Ratio
# 
# 
# 
def Stall_Beginning(solv_vars, vars, dict_val):
	eta_stall = vars[0]
	lambda_ = vars[1]

	eq = Eq(eta_stall, 1-lambda_)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Stall Beginning')
vars_names['Stall Beginning'] = ['Stall Begin', 'Taper Ratio']
variables['Stall Beginning'] = ['eta_stall', 'lambda_']
formulas['Stall Beginning'] = 'eta_stall = 1-lambda_'
num_vars['Stall Beginning'] = 2
equations['Stall Beginning'] = Stall_Beginning
# 
# 
# 
def Wing_Twist_Geometric(solv_vars, vars, dict_val):
	alpha_r = vars[0]
	alpha_t = vars[1]
	epsilon_g = vars[2]

	eq = Eq(epsilon_g, alpha_t-alpha_r)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Wing Twist Geometric')
vars_names['Wing Twist Geometric'] = ['Root Incidence', 'Tip Incidence', 'Wing Twist Geometric']
variables['Wing Twist Geometric'] = ['alpha_r', 'alpha_t', 'epsilon_g']
formulas['Wing Twist Geometric'] = 'epsilon_g = alpha_t-alpha_r'
num_vars['Wing Twist Geometric'] = 3
equations['Wing Twist Geometric'] = Wing_Twist_Geometric
# 
# 
# 
def Wing_Twist_Aerodynamic(solv_vars, vars, dict_val):
	alpha_0_r = vars[0]
	alpha_0_t = vars[1]
	epsilon_a = vars[2]
	epsilon_g = vars[3]

	eq = Eq(epsilon_a, epsilon_g+alpha_0_t-alpha_0_r)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Wing Twist Aerodynamic')
vars_names['Wing Twist Aerodynamic'] = ['unknow_1', 'unknow_2', 'Wing Twist Aerodynamic', 'Wing Twist Geometric']
variables['Wing Twist Aerodynamic'] = ['alpha_0_r', 'alpha_0_t', 'epsilon_a', 'epsilon_g']
formulas['Wing Twist Aerodynamic'] = 'epsilon_a = epsilon_g+alpha_0_t-alpha_0_r'
num_vars['Wing Twist Aerodynamic'] = 4
equations['Wing Twist Aerodynamic'] = Wing_Twist_Aerodynamic
# 
# 
# 
def Ground_Effect_Parameter(solv_vars, vars, dict_val):
	b = vars[0]
	h = vars[1]
	phi = vars[2]

	eq = Eq(phi, (16*h/b)**2/(1+(16*h/b)**2))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Ground Effect Parameter')
vars_names['Ground Effect Parameter'] = ['Span', 'Wing High', 'Wing Twist Aerodynamic']
variables['Ground Effect Parameter'] = ['b', 'h', 'phi']
formulas['Ground Effect Parameter'] = 'phi = (16*h/b)**2/(1+(16*h/b)**2)'
num_vars['Ground Effect Parameter'] = 3
equations['Ground Effect Parameter'] = Ground_Effect_Parameter
# 
# 
# 
def Wing_Load(solv_vars, vars, dict_val):
	S = vars[0]
	W = vars[1]
	wl = vars[2]

	eq = Eq(wl, W/S)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Wing Load')
vars_names['Wing Load'] = ['Area', 'Weight', 'Wing load']
variables['Wing Load'] = ['S', 'W', 'wl']
formulas['Wing Load'] = 'wl = W/S'
num_vars['Wing Load'] = 3
equations['Wing Load'] = Wing_Load
# 
# 
# 
