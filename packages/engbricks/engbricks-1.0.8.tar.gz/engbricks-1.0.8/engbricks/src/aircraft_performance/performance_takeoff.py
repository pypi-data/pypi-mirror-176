from sympy import Eq, solve
from sympy import sin, cos, tan, atan, ln, pi, sqrt, integrate
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
def Speed_Lift_Off(solv_vars, vars, dict_val):
	V_LO = vars[0]
	V_s = vars[1]

	eq = Eq(V_LO, 1.2*V_s)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed Lift Off')
vars_names['Speed Lift Off'] = ['Lift-off Speed', 'Stall Speed']
variables['Speed Lift Off'] = ['V_LO', 'V_s']
formulas['Speed Lift Off'] = 'V_LO = 1.2*V_s'
num_vars['Speed Lift Off'] = 2
equations['Speed Lift Off'] = Speed_Lift_Off
# 
# 
# 
def Acceleration_Distance(solv_vars, vars, dict_val):
	D = vars[0]
	L = vars[1]
	T = vars[2]
	V = vars[3]
	W = vars[4]
	g = vars[5]
	miu = vars[6]
	s_acel = vars[7]

	eq = Eq(s_acel, integrate(W/(2*g*(T-D-miu*(W-L))),V))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Acceleration Distance')
vars_names['Acceleration Distance'] = ['Drag', 'Lift', 'Thrust', 'Speed', 'Weight', 'Gravity Acc', 'Coef Friction', 'Accel Dist']
variables['Acceleration Distance'] = ['D', 'L', 'T', 'V', 'W', 'g', 'miu', 's_acel']
formulas['Acceleration Distance'] = 's_acel = integral(W/(2*g*(T-D-miu*(W-L))),V)'
num_vars['Acceleration Distance'] = 8
equations['Acceleration Distance'] = Acceleration_Distance
# 
# 
# 
def Acceleration_Time(solv_vars, vars, dict_val):
	D = vars[0]
	L = vars[1]
	T = vars[2]
	V = vars[3]
	W = vars[4]
	g = vars[5]
	miu = vars[6]
	t_acel = vars[7]

	eq = Eq(t_acel, integrate(W/(g*(T-D-miu*(W-L))),V))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Acceleration Time')
vars_names['Acceleration Time'] = ['Drag', 'Lift', 'Thrust', 'Speed', 'Weight', 'Gravity Acc', 'Coef Friction', 'Accel Time']
variables['Acceleration Time'] = ['D', 'L', 'T', 'V', 'W', 'g', 'miu', 't_acel']
formulas['Acceleration Time'] = 't_acel = integral(W/(g*(T-D-miu*(W-L))),V)'
num_vars['Acceleration Time'] = 8
equations['Acceleration Time'] = Acceleration_Time
# 
# 
# 
def Rotation_Distance(solv_vars, vars, dict_val):
	V_LO = vars[0]
	s_rot = vars[1]
	t_rot = vars[2]

	eq = Eq(s_rot, V_LO*t_rot)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Rotation Distance')
vars_names['Rotation Distance'] = ['Lift-off Speed', 'Rot Dist', 'Rot Time']
variables['Rotation Distance'] = ['V_LO', 's_rot', 't_rot']
formulas['Rotation Distance'] = 's_rot = V_LO*t_rot'
num_vars['Rotation Distance'] = 3
equations['Rotation Distance'] = Rotation_Distance
# 
# 
# 
def Rotation_Time(solv_vars, vars, dict_val):
	t_rot = vars[0]

	eq = Eq(t_rot, 3)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Rotation Time')
vars_names['Rotation Time'] = ['Rot Time']
variables['Rotation Time'] = ['t_rot']
formulas['Rotation Time'] = 't_rot = 3'
num_vars['Rotation Time'] = 1
equations['Rotation Time'] = Rotation_Time
# 
# 
# 
def Transition_Distance(solv_vars, vars, dict_val):
	r = vars[0]
	s_trans = vars[1]
	theta_trans = vars[2]

	eq = Eq(s_trans, r*sin(theta_trans))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Transition Distance')
vars_names['Transition Distance'] = ['Radius', 'Trans Dist', 'Trans Angle']
variables['Transition Distance'] = ['r', 's_trans', 'theta_trans']
formulas['Transition Distance'] = 's_trans = r*sin(theta_trans)'
num_vars['Transition Distance'] = 3
equations['Transition Distance'] = Transition_Distance
# 
# 
# 
def Transition_Time(solv_vars, vars, dict_val):
	V_LO = vars[0]
	r = vars[1]
	t_trans = vars[2]
	theta_trans = vars[3]

	eq = Eq(t_trans, r*theta_trans/V_LO)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Transition Time')
vars_names['Transition Time'] = ['Lift-off Speed', 'Radius', 'Trans Time', 'Trans Angle']
variables['Transition Time'] = ['V_LO', 'r', 't_trans', 'theta_trans']
formulas['Transition Time'] = 't_trans = r*theta_trans/V_LO'
num_vars['Transition Time'] = 4
equations['Transition Time'] = Transition_Time
# 
# 
# 
def Climb_Distance(solv_vars, vars, dict_val):
	h_OB = vars[0]
	r = vars[1]
	s_climb = vars[2]
	theta_trans = vars[3]

	eq = Eq(s_climb, (h_OB-r*(1-cos(theta_trans)))/(tan(theta_trans)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Climb Distance')
vars_names['Climb Distance'] = ['Obstacle Height', 'Radius', 'Climb Dist', 'Trans Angle']
variables['Climb Distance'] = ['h_OB', 'r', 's_climb', 'theta_trans']
formulas['Climb Distance'] = 's_climb = (h_OB-r*(1-cos(theta_trans)))/(tan(theta_trans))'
num_vars['Climb Distance'] = 4
equations['Climb Distance'] = Climb_Distance
# 
# 
# 
def Climb_Time(solv_vars, vars, dict_val):
	V_LO = vars[0]
	h_OB = vars[1]
	r = vars[2]
	t_climb = vars[3]
	theta_trans = vars[4]

	eq = Eq(t_climb, (h_OB-r*(1-cos(theta_trans)))/(V_LO*sin(theta_trans)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Climb Time')
vars_names['Climb Time'] = ['Lift-off Speed', 'Obstacle Height', 'Radius', 'Climb Time', 'Trans Angle']
variables['Climb Time'] = ['V_LO', 'h_OB', 'r', 't_climb', 'theta_trans']
formulas['Climb Time'] = 't_climb = (h_OB-r*(1-cos(theta_trans)))/(V_LO*sin(theta_trans))'
num_vars['Climb Time'] = 5
equations['Climb Time'] = Climb_Time
# 
# 
# 
def Rotation_Radius(solv_vars, vars, dict_val):
	V_LO = vars[0]
	g = vars[1]
	n = vars[2]
	r = vars[3]

	eq = Eq(r, V_LO**2/(g*(n-1)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Rotation Radius')
vars_names['Rotation Radius'] = ['Lift-off Speed', 'Gravity Acc', 'Load Factor', 'Radius']
variables['Rotation Radius'] = ['V_LO', 'g', 'n', 'r']
formulas['Rotation Radius'] = 'r = V_LO**2/(g*(n-1))'
num_vars['Rotation Radius'] = 4
equations['Rotation Radius'] = Rotation_Radius
# 
# 
# 
def Obstacle_Angle(solv_vars, vars, dict_val):
	h_OB = vars[0]
	r = vars[1]
	theta_OB = vars[2]

	eq = Eq(cos(theta_OB), (r-h_OB)/r)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Obstacle Angle')
vars_names['Obstacle Angle'] = ['Obstacle Height', 'Radius', 'Obstacle Angle']
variables['Obstacle Angle'] = ['h_OB', 'r', 'theta_OB']
formulas['Obstacle Angle'] = 'cos(theta_OB) = (r-h_OB)/r'
num_vars['Obstacle Angle'] = 3
equations['Obstacle Angle'] = Obstacle_Angle
# 
# 
# 
def Jet_Transition_Angle(solv_vars, vars, dict_val):
	E_LO = vars[0]
	T = vars[1]
	W = vars[2]
	theta_trans = vars[3]

	eq = Eq(sin(theta_trans/0.9), T/W-1/E_LO)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Transition Angle')
vars_names['Jet Transition Angle'] = ['LO Efficiency', 'Thrust', 'Weight', 'Trans Angle']
variables['Jet Transition Angle'] = ['E_LO', 'T', 'W', 'theta_trans']
formulas['Jet Transition Angle'] = 'sin(theta_trans/0.9) = T/W-1/E_LO'
num_vars['Jet Transition Angle'] = 4
equations['Jet Transition Angle'] = Jet_Transition_Angle
# 
# 
# 
def Propeller_Transition_Angle(solv_vars, vars, dict_val):
	E_LO = vars[0]
	P_e = vars[1]
	V_LO = vars[2]
	W = vars[3]
	eta_P = vars[4]
	theta_trans = vars[5]

	eq = Eq(sin(theta_trans/0.9), (eta_P*P_e)/(W*V_LO)-1/E_LO)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Propeller Transition Angle')
vars_names['Propeller Transition Angle'] = ['LO Efficiency', 'Power effective', 'Lift-off Speed', 'Weight', 'Populsive Efficiency', 'Trans Angle']
variables['Propeller Transition Angle'] = ['E_LO', 'P_e', 'V_LO', 'W', 'eta_P', 'theta_trans']
formulas['Propeller Transition Angle'] = 'sin(theta_trans/0.9) = (eta_P*P_e)/(W*V_LO)-1/E_LO'
num_vars['Propeller Transition Angle'] = 6
equations['Propeller Transition Angle'] = Propeller_Transition_Angle
# 
# 
# 
