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
def V_T_Volume_Coef(solv_vars, vars, dict_val):
	L_v = vars[0]
	S_v = vars[1]
	S_w = vars[2]
	V_v = vars[3]
	b = vars[4]

	eq = Eq(V_v, S_v*L_v/(S_w*b))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('V.T. Volume Coef')
vars_names['V.T. Volume Coef'] = ['VT a.c. to c.g.', 'VT Area', 'Wing Area', 'VT Volume Coef.', 'Span']
variables['V.T. Volume Coef'] = ['L_v', 'S_v', 'S_w', 'V_v', 'b']
formulas['V.T. Volume Coef'] = 'V_v = S_v*L_v/(S_w*b)'
num_vars['V.T. Volume Coef'] = 5
equations['V.T. Volume Coef'] = V_T_Volume_Coef
# 
# 
# 
def H_T_Volume_Coef(solv_vars, vars, dict_val):
	L_h = vars[0]
	S_h = vars[1]
	S_w = vars[2]
	V_h = vars[3]
	mac = vars[4]

	eq = Eq(V_h, S_h*L_h/(S_w*mac))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('H.T. Volume Coef')
vars_names['H.T. Volume Coef'] = ['HT a.c. to c.g.', 'HT Area', 'Wing Area', 'HT Volume Coef.', 'mean aerodynamic chord']
variables['H.T. Volume Coef'] = ['L_h', 'S_h', 'S_w', 'V_h', 'mac']
formulas['H.T. Volume Coef'] = 'V_h = S_h*L_h/(S_w*mac)'
num_vars['H.T. Volume Coef'] = 5
equations['H.T. Volume Coef'] = H_T_Volume_Coef
# 
# 
# 