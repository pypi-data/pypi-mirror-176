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
def Radius(solv_vars, vars, dict_val):
	V = vars[0]
	g = vars[1]
	n = vars[2]
	r = vars[3]

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Radius')
vars_names['Radius'] = ['Speed', 'Gravity Acc', 'Load Factor', 'Radius']
variables['Radius'] = ['V', 'g', 'n', 'r']
formulas['Radius'] = 'r = V**2/(g*sqrt(n**2-1))'
num_vars['Radius'] = 4
equations['Radius'] = Radius
# 
# 
# 
def Rate(solv_vars, vars, dict_val):
	V = vars[0]
	omega = vars[1]
	r = vars[2]

	eq = Eq(omega, V/r)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Rate')
vars_names['Rate'] = ['Speed', 'Turn Rate Change', 'Radius']
variables['Rate'] = ['V', 'omega', 'r']
formulas['Rate'] = 'omega = V/r'
num_vars['Rate'] = 3
equations['Rate'] = Rate
# 
# 
# 
def Roll_Angle(solv_vars, vars, dict_val):
	n = vars[0]
	phi = vars[1]

	eq = Eq(cos(phi), 1/n)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Roll Angle')
vars_names['Roll Angle'] = ['Load Factor', 'Wing Twist Aerodynamic']
variables['Roll Angle'] = ['n', 'phi']
formulas['Roll Angle'] = 'cos(phi) = 1/n'
num_vars['Roll Angle'] = 2
equations['Roll Angle'] = Roll_Angle
# 
# 
# 
def Load_Factor_Stall_Turn(solv_vars, vars, dict_val):
	E_C_L_max = vars[0]
	T_A = vars[1]
	W = vars[2]
	n_ST = vars[3]

	eq = Eq(n_ST, T_A/W*E_C_L_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Load Factor Stall Turn')
vars_names['Load Factor Stall Turn'] = ['Efficiency C_L Max', 'Thrust Available variables', 'Weight', 'Load Factor Stall Turn']
variables['Load Factor Stall Turn'] = ['E_C_L_max', 'T_A', 'W', 'n_ST']
formulas['Load Factor Stall Turn'] = 'n_ST = T_A/W*E_C_L_max'
num_vars['Load Factor Stall Turn'] = 4
equations['Load Factor Stall Turn'] = Load_Factor_Stall_Turn
# 
# 
# 
def Speed_Stall_Turn(solv_vars, vars, dict_val):
	C_L_max = vars[0]
	E_C_L_max = vars[1]
	S = vars[2]
	T_A = vars[3]
	V_ST = vars[4]
	W = vars[5]
	rho_0 = vars[6]
	sigma = vars[7]

	eq = Eq(V_ST, sqrt((2*(T_A/W)*(W/S)*E_C_L_max)/(rho_0*sigma*C_L_max)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed Stall Turn')
vars_names['Speed Stall Turn'] = ['Max C_L', 'Efficiency C_L Max', 'Area', 'Thrust Available variables', 'Speed Stall Turn', 'Weight', 'Air Density Sea Level', 'sigma']
variables['Speed Stall Turn'] = ['C_L_max', 'E_C_L_max', 'S', 'T_A', 'V_ST', 'W', 'rho_0', 'sigma']
formulas['Speed Stall Turn'] = 'V_ST = sqrt((2*(T_A/W)*(W/S)*E_C_L_max)/(rho_0*sigma*C_L_max))'
num_vars['Speed Stall Turn'] = 8
equations['Speed Stall Turn'] = Speed_Stall_Turn
# 
# 
# 
def Load_Factor_Fast_Turn(solv_vars, vars, dict_val):
	n_m = vars[0]
	n_FT = vars[1]

	eq = Eq(n_FT, sqrt(2*n_m-1))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Load Factor Fast Turn')
vars_names['Load Factor Fast Turn'] = ['Load Factor', 'Load Factor Fast Turn']
variables['Load Factor Fast Turn'] = ['n_m', 'n_FT']
formulas['Load Factor Fast Turn'] = 'n_FT = sqrt(2*n_m-1)'
num_vars['Load Factor Fast Turn'] = 2
equations['Load Factor Fast Turn'] = Load_Factor_Fast_Turn
# 
# 
# 
def Speed_Fast_Turn(solv_vars, vars, dict_val):
	C_D0 = vars[0]
	K = vars[1]
	S = vars[2]
	V_FT = vars[3]
	W = vars[4]
	rho_0 = vars[5]
	sigma = vars[6]

	eq = Eq(V_FT, sqrt(2*(W/S)/(rho_0*sigma))*(K/C_D0)**(1/4))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed Fast Turn')
vars_names['Speed Fast Turn'] = ['Parasite Drag Coefficient', 'Induced Drag Factor', 'Area', 'Speed Fast Turn', 'Weight', 'Air Density Sea Level', 'sigma']
variables['Speed Fast Turn'] = ['C_D0', 'K', 'S', 'V_FT', 'W', 'rho_0', 'sigma']
formulas['Speed Fast Turn'] = 'V_FT = sqrt(2*(W/S)/(rho_0*sigma))*(K/C_D0)**(1/4)'
num_vars['Speed Fast Turn'] = 7
equations['Speed Fast Turn'] = Speed_Fast_Turn
# 
# 
# 
def Roll_Angle_Fast_Turn(solv_vars, vars, dict_val):
	n_FT = vars[0]
	phi_FT = vars[1]

	eq = Eq(cos(phi_FT), 1/n_FT)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Roll Angle Fast Turn')
vars_names['Roll Angle Fast Turn'] = ['Load Factor Fast Turn', 'Angle Fast Turn']
variables['Roll Angle Fast Turn'] = ['n_FT', 'phi_FT']
formulas['Roll Angle Fast Turn'] = 'cos(phi_FT) = 1/n_FT'
num_vars['Roll Angle Fast Turn'] = 2
equations['Roll Angle Fast Turn'] = Roll_Angle_Fast_Turn
# 
# 
# 
def Lift_Coefficient_Fast_Turn(solv_vars, vars, dict_val):
	C_L_E_max = vars[0]
	C_L_FT = vars[1]
	n_FT = vars[2]

	eq = Eq(C_L_FT, n_FT*C_L_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Lift Coefficient Fast Turn')
vars_names['Lift Coefficient Fast Turn'] = ['Max Efficiency C_L', 'C_L Fast Turn', 'Load Factor Fast Turn']
variables['Lift Coefficient Fast Turn'] = ['C_L_E_max', 'C_L_FT', 'n_FT']
formulas['Lift Coefficient Fast Turn'] = 'C_L_FT = n_FT*C_L_E_max'
num_vars['Lift Coefficient Fast Turn'] = 3
equations['Lift Coefficient Fast Turn'] = Lift_Coefficient_Fast_Turn
# 
# 
# 
def Load_Factor_Tight_Turn(solv_vars, vars, dict_val):
	E_max = vars[0]
	T = vars[1]
	W = vars[2]
	n_TT = vars[3]

	eq = Eq(n_TT, sqrt(2-1/(E_max**2*(T/W)**2)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Load Factor Tight Turn')
vars_names['Load Factor Tight Turn'] = ['Max Efficiency', 'Thrust', 'Weight', 'Load Factor Tight Turn']
variables['Load Factor Tight Turn'] = ['E_max', 'T', 'W', 'n_TT']
formulas['Load Factor Tight Turn'] = 'n_TT = sqrt(2-1/(E_max**2*(T/W)**2))'
num_vars['Load Factor Tight Turn'] = 4
equations['Load Factor Tight Turn'] = Load_Factor_Tight_Turn
# 
# 
# 
def Speed_Tight_Turn(solv_vars, vars, dict_val):
	K = vars[0]
	S = vars[1]
	T = vars[2]
	V_TT = vars[3]
	W = vars[4]
	rho_0 = vars[5]
	sigma = vars[6]

	eq = Eq(V_TT, 2*sqrt(K*(W/S)/(rho_0*sigma*(T/W))))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed Tight Turn')
vars_names['Speed Tight Turn'] = ['Induced Drag Factor', 'Area', 'Thrust', 'Speed Tight Turn', 'Weight', 'Air Density Sea Level', 'sigma']
variables['Speed Tight Turn'] = ['K', 'S', 'T', 'V_TT', 'W', 'rho_0', 'sigma']
formulas['Speed Tight Turn'] = 'V_TT = 2*sqrt(K*(W/S)/(rho_0*sigma*(T/W)))'
num_vars['Speed Tight Turn'] = 7
equations['Speed Tight Turn'] = Speed_Tight_Turn
# 
# 
# 
def Roll_Angle_Tight_Turn(solv_vars, vars, dict_val):
	n_TT = vars[0]
	phi_TT = vars[1]

	eq = Eq(cos(phi_TT), 1/n_TT)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Roll Angle Tight Turn')
vars_names['Roll Angle Tight Turn'] = ['Load Factor Tight Turn', 'Angle Tight Turn']
variables['Roll Angle Tight Turn'] = ['n_TT', 'phi_TT']
formulas['Roll Angle Tight Turn'] = 'cos(phi_TT) = 1/n_TT'
num_vars['Roll Angle Tight Turn'] = 2
equations['Roll Angle Tight Turn'] = Roll_Angle_Tight_Turn
# 
# 
# 
def Lift_Coefficient_Tight_Turn(solv_vars, vars, dict_val):
	C_L_TT = vars[0]
	K = vars[1]
	T = vars[2]
	W = vars[3]
	n_TT = vars[4]

	eq = Eq(C_L_TT, (T/W)*n_TT/(2*K))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Lift Coefficient Tight Turn')
vars_names['Lift Coefficient Tight Turn'] = ['C_L Tight Turn', 'Induced Drag Factor', 'Thrust', 'Weight', 'Load Factor Tight Turn']
variables['Lift Coefficient Tight Turn'] = ['C_L_TT', 'K', 'T', 'W', 'n_TT']
formulas['Lift Coefficient Tight Turn'] = 'C_L_TT = (T/W)*n_TT/(2*K)'
num_vars['Lift Coefficient Tight Turn'] = 5
equations['Lift Coefficient Tight Turn'] = Lift_Coefficient_Tight_Turn
# 
# 
# 
def Propeller_Load_Factor_Stall_Turn(solv_vars, vars, dict_val):
	C_L_max = vars[0]
	E_C_L_max = vars[1]
	P_e = vars[2]
	S = vars[3]
	V_ST = vars[4]
	W = vars[5]
	eta_P = vars[6]
	rho_0 = vars[7]
	sigma = vars[8]

	eq = Eq(V_ST, ((2*eta_P*(P_e/W)*(W/S)*E_C_L_max)/(rho_0*sigma*C_L_max))**1/3)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Load Factor Stall Turn')
vars_names['Propeller Load Factor Stall Turn'] = ['Max C_L', 'Efficiency C_L Max', 'Power effective', 'Area', 'Speed Stall Turn', 'Weight', 'Populsive Efficiency', 'Air Density Sea Level', 'sigma']
variables['Propeller Load Factor Stall Turn'] = ['C_L_max', 'E_C_L_max', 'P_e', 'S', 'V_ST', 'W', 'eta_P', 'rho_0', 'sigma']
formulas['Propeller Load Factor Stall Turn'] = 'V_ST = ((2*eta_P*(P_e/W)*(W/S)*E_C_L_max)/(rho_0*sigma*C_L_max))**1/3'
num_vars['Propeller Load Factor Stall Turn'] = 9
equations['Propeller Load Factor Stall Turn'] = Propeller_Load_Factor_Stall_Turn
# 
# 
# 
def Propeller_Speed_Stall_Turn(solv_vars, vars, dict_val):
	C_L_max = vars[0]
	E_C_L_max = vars[1]
	P_e = vars[2]
	S = vars[3]
	W = vars[4]
	eta_P = vars[5]
	n_ST = vars[6]
	rho_0 = vars[7]
	sigma = vars[8]

	eq = Eq(n_ST, (rho_0*sigma*C_L_max)/(2*(W/S))*((2*eta_P*(P_e/W)*(W/S)*E_C_L_max)/(rho_0*sigma*C_L_max))**2/3)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Speed Stall Turn')
vars_names['Propeller Speed Stall Turn'] = ['Max C_L', 'Efficiency C_L Max', 'Power effective', 'Area', 'Weight', 'Populsive Efficiency', 'Load Factor Stall Turn', 'Air Density Sea Level', 'sigma']
variables['Propeller Speed Stall Turn'] = ['C_L_max', 'E_C_L_max', 'P_e', 'S', 'W', 'eta_P', 'n_ST', 'rho_0', 'sigma']
formulas['Propeller Speed Stall Turn'] = 'n_ST = (rho_0*sigma*C_L_max)/(2*(W/S))*((2*eta_P*(P_e/W)*(W/S)*E_C_L_max)/(rho_0*sigma*C_L_max))**2/3'
num_vars['Propeller Speed Stall Turn'] = 9
equations['Propeller Speed Stall Turn'] = Propeller_Speed_Stall_Turn
# 
# 
# 
def Propeller_Speed_Fast_Turn(solv_vars, vars, dict_val):
	K = vars[0]
	P_e = vars[1]
	S = vars[2]
	V_FT = vars[3]
	W = vars[4]
	eta_P = vars[5]
	rho_0 = vars[6]
	sigma = vars[7]

	eq = Eq(V_FT, ((4*K*(W/S))/(eta_P*(P_e/W)*rho_0*sigma))**1/3)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Speed Fast Turn')
vars_names['Propeller Speed Fast Turn'] = ['Induced Drag Factor', 'Power effective', 'Area', 'Speed Fast Turn', 'Weight', 'Populsive Efficiency', 'Air Density Sea Level', 'sigma']
variables['Propeller Speed Fast Turn'] = ['K', 'P_e', 'S', 'V_FT', 'W', 'eta_P', 'rho_0', 'sigma']
formulas['Propeller Speed Fast Turn'] = 'V_FT = ((4*K*(W/S))/(eta_P*(P_e/W)*rho_0*sigma))**1/3'
num_vars['Propeller Speed Fast Turn'] = 8
equations['Propeller Speed Fast Turn'] = Propeller_Speed_Fast_Turn
# 
# 
# 
def Propeller_Load_Factor_Fast_Turn(solv_vars, vars, dict_val):
	E_max = vars[0]
	K = vars[1]
	P_e = vars[2]
	S = vars[3]
	W = vars[4]
	eta_P = vars[5]
	n_FT = vars[6]
	rho_0 = vars[7]
	sigma = vars[8]

	eq = Eq(n_FT, (2-(4*K*(W/S))/((eta_P*(P_e/W))**2*rho_0*sigma*E_max))**1/2)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Load Factor Fast Turn')
vars_names['Propeller Load Factor Fast Turn'] = ['Max Efficiency', 'Induced Drag Factor', 'Power effective', 'Area', 'Weight', 'Populsive Efficiency', 'Load Factor Fast Turn', 'Air Density Sea Level', 'sigma']
variables['Propeller Load Factor Fast Turn'] = ['E_max', 'K', 'P_e', 'S', 'W', 'eta_P', 'n_FT', 'rho_0', 'sigma']
formulas['Propeller Load Factor Fast Turn'] = 'n_FT = (2-(4*K*(W/S))/((eta_P*(P_e/W))**2*rho_0*sigma*E_max))**1/2'
num_vars['Propeller Load Factor Fast Turn'] = 9
equations['Propeller Load Factor Fast Turn'] = Propeller_Load_Factor_Fast_Turn
# 
# 
# 
def Propeller_Roll_Angle_Fast_Turn(solv_vars, vars, dict_val):
	n_FT = vars[0]
	phi_FT = vars[1]

	eq = Eq(cos(phi_FT), 1/n_FT)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Roll Angle Fast Turn')
vars_names['Propeller Roll Angle Fast Turn'] = ['Load Factor Fast Turn', 'Angle Fast Turn']
variables['Propeller Roll Angle Fast Turn'] = ['n_FT', 'phi_FT']
formulas['Propeller Roll Angle Fast Turn'] = 'cos(phi_FT) = 1/n_FT'
num_vars['Propeller Roll Angle Fast Turn'] = 2
equations['Propeller Roll Angle Fast Turn'] = Propeller_Roll_Angle_Fast_Turn
# 
# 
# 
def Propeller_Lift_Coefficient_Fast_Turn(solv_vars, vars, dict_val):
	C_L_E_max = vars[0]
	C_L_FT = vars[1]
	n_FT = vars[2]

	eq = Eq(C_L_FT, n_FT*C_L_E_max)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Lift Coefficient Fast Turn')
vars_names['Propeller Lift Coefficient Fast Turn'] = ['Max Efficiency C_L', 'C_L Fast Turn', 'Load Factor Fast Turn']
variables['Propeller Lift Coefficient Fast Turn'] = ['C_L_E_max', 'C_L_FT', 'n_FT']
formulas['Propeller Lift Coefficient Fast Turn'] = 'C_L_FT = n_FT*C_L_E_max'
num_vars['Propeller Lift Coefficient Fast Turn'] = 3
equations['Propeller Lift Coefficient Fast Turn'] = Propeller_Lift_Coefficient_Fast_Turn
# 
# 
# 
def Propeller_Speed_Tight_Turn(solv_vars, vars, dict_val):
	K = vars[0]
	P_e = vars[1]
	S = vars[2]
	V_TT = vars[3]
	W = vars[4]
	eta_P = vars[5]
	rho_0 = vars[6]
	sigma = vars[7]

	eq = Eq(V_TT, (8*K*(W/S))/(3*eta_P*rho_0*sigma*(P_e/W)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Speed Tight Turn')
vars_names['Propeller Speed Tight Turn'] = ['Induced Drag Factor', 'Power effective', 'Area', 'Speed Tight Turn', 'Weight', 'Populsive Efficiency', 'Air Density Sea Level', 'sigma']
variables['Propeller Speed Tight Turn'] = ['K', 'P_e', 'S', 'V_TT', 'W', 'eta_P', 'rho_0', 'sigma']
formulas['Propeller Speed Tight Turn'] = 'V_TT = (8*K*(W/S))/(3*eta_P*rho_0*sigma*(P_e/W))'
num_vars['Propeller Speed Tight Turn'] = 8
equations['Propeller Speed Tight Turn'] = Propeller_Speed_Tight_Turn
# 
# 
# 
def Propeller_Load_Factor_Tight_Turn(solv_vars, vars, dict_val):
	E_max = vars[0]
	K = vars[1]
	P_e = vars[2]
	S = vars[3]
	W = vars[4]
	eta_P = vars[5]
	n_TT = vars[6]
	rho_0 = vars[7]
	sigma = vars[8]

	eq = Eq(n_TT, (4/3-((1.78*K*(W/S))/((eta_P*(P_e/W))**2*rho_0*sigma*E_max))**2)**1/2)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Load Factor Tight Turn')
vars_names['Propeller Load Factor Tight Turn'] = ['Max Efficiency', 'Induced Drag Factor', 'Power effective', 'Area', 'Weight', 'Populsive Efficiency', 'Load Factor Tight Turn', 'Air Density Sea Level', 'sigma']
variables['Propeller Load Factor Tight Turn'] = ['E_max', 'K', 'P_e', 'S', 'W', 'eta_P', 'n_TT', 'rho_0', 'sigma']
formulas['Propeller Load Factor Tight Turn'] = 'n_TT = (4/3-((1.78*K*(W/S))/((eta_P*(P_e/W))**2*rho_0*sigma*E_max))**2)**1/2'
num_vars['Propeller Load Factor Tight Turn'] = 9
equations['Propeller Load Factor Tight Turn'] = Propeller_Load_Factor_Tight_Turn
# 
# 
# 
def Propeller_Roll_Angle_Tight_Turn(solv_vars, vars, dict_val):
	n_TT = vars[0]
	phi_TT = vars[1]

	eq = Eq(cos(phi_TT), 1/n_TT)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Roll Angle Tight Turn')
vars_names['Propeller Roll Angle Tight Turn'] = ['Load Factor Tight Turn', 'Angle Tight Turn']
variables['Propeller Roll Angle Tight Turn'] = ['n_TT', 'phi_TT']
formulas['Propeller Roll Angle Tight Turn'] = 'cos(phi_TT) = 1/n_TT'
num_vars['Propeller Roll Angle Tight Turn'] = 2
equations['Propeller Roll Angle Tight Turn'] = Propeller_Roll_Angle_Tight_Turn
# 
# 
# 
def Propeller_Lift_Coefficient_Tight_Turn(solv_vars, vars, dict_val):
	C_L_TT = vars[0]
	K = vars[1]
	P_e = vars[2]
	V = vars[3]
	W = vars[4]
	eta_P = vars[5]
	n_TT = vars[6]

	eq = Eq(C_L_TT, eta_P*(P_e/W)*n_TT/(2*K*V))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Lift Coefficient Tight Turn')
vars_names['Propeller Lift Coefficient Tight Turn'] = ['C_L Tight Turn', 'Induced Drag Factor', 'Power effective', 'Speed', 'Weight', 'Populsive Efficiency', 'Load Factor Tight Turn']
variables['Propeller Lift Coefficient Tight Turn'] = ['C_L_TT', 'K', 'P_e', 'V', 'W', 'eta_P', 'n_TT']
formulas['Propeller Lift Coefficient Tight Turn'] = 'C_L_TT = eta_P*(P_e/W)*n_TT/(2*K*V)'
num_vars['Propeller Lift Coefficient Tight Turn'] = 7
equations['Propeller Lift Coefficient Tight Turn'] = Propeller_Lift_Coefficient_Tight_Turn
# 
# 
# 
