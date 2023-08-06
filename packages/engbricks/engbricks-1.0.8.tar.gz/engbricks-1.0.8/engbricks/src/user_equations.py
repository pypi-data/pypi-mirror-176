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
def Intake_Temperature(solv_vars, vars, dict_val):
	C_a = vars[0]
	T_a = vars[1]
	T_intake = vars[2]
	cp_a = vars[3]

	eq = Eq(T_intake, T_a+C_a**2/(2*cp_a))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Intake Temperature')
vars_names['Intake Temperature'] = ['Aircraft Speed', 'Admission Temperature', 'Aft Intake Temperature', 'Fresh air SHC']
variables['Intake Temperature'] = ['C_a', 'T_a', 'T_intake', 'cp_a']
formulas['Intake Temperature'] = 'T_intake = T_a+C_a**2/(2*cp_a)'
num_vars['Intake Temperature'] = 4
equations['Intake Temperature'] = Intake_Temperature