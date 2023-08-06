from sympy import Eq, solve
from sympy import sin, cos, tan, atan, ln, pi, sqrt, exp, Pow
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
def Temp_to_11km(solv_vars, vars, dict_val):
	h = vars[0]
	lambda_1 = vars[1]
	T_0 = vars[2]
	T_0_11k = vars[3]

	eq = Eq(T_0_11k, T_0+lambda_1*h)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Temp to 11km')
vars_names['Temp to 11km'] = ['Altitude', 'lambda_1', 'Temp at 0m', 'Temp to 11km']
variables['Temp to 11km'] = ['h', 'lambda_1', 'T_0', 'T_0_11k']
formulas['Temp to 11km'] = 'T_0_11k = T_0+lambda_1*h'
num_vars['Temp to 11km'] = 4
equations['Temp to 11km'] = Temp_to_11km
# 
# 
# 
def Temp_to_20km(solv_vars, vars, dict_val):
	h = vars[0]
	lambda_2 = vars[1]
	T_11k = vars[2]
	T_11_20k = vars[3]

	eq = Eq(T_11_20k, T_11k+lambda_2*h)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Temp to 20km')
vars_names['Temp to 20km'] = ['Altitude', 'lambda_2', 'Temp at 11km', 'Temp to 20km']
variables['Temp to 20km'] = ['h', 'lambda_2', 'T_11k', 'T_11_20k']
formulas['Temp to 20km'] = 'T_11_20k = T_11k+lambda_2*h'
num_vars['Temp to 20km'] = 4
equations['Temp to 20km'] = Temp_to_20km
# 
# 
# 
def Temp_to_32km(solv_vars, vars, dict_val):
	h = vars[0]
	lambda_3 = vars[1]
	T_20k = vars[2]
	T_20_32k = vars[3]

	eq = Eq(T_20_32k, T_20k+lambda_3*(h-20000))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Temp to 32km')
vars_names['Temp to 32km'] = ['Altitude', 'lambda_3', 'Temp at 20km', 'Temp to 32km']
variables['Temp to 32km'] = ['h', 'lambda_3', 'T_20k', 'T_20_32k']
formulas['Temp to 32km'] = 'T_20_32k = T_20k+lambda_3*(h-20000)'
num_vars['Temp to 32km'] = 4
equations['Temp to 32km'] = Temp_to_32km
# 
# 
# 
def Pressure_to_11km(solv_vars, vars, dict_val):
	t = vars[0]
	grav_acc = vars[1]
	gas_constant = vars[2]
	lambda_1 = vars[3]
	T_0 = vars[4]
	p_0 = vars[5]
	p_0_11k = vars[6]

	eq = Eq(p_0_11k, p_0*Pow((t/T_0),(-grav_acc/lambda_1/gas_constant)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results
# 
# 
# 
names.append('Pressure to 11km')
vars_names['Pressure to 11km'] = ['Temperatue', 'Gravitational acceleration', 'Gas Constant', 'lambda_1', 'Temp at 0m', 'Pressure at 0m', 'Pressure to 11km']
variables['Pressure to 11km'] = ['t', 'grav_acc', 'gas_constant', 'lambda_1', 'T_0', 'p_0', 'p_0_11k']
formulas['Pressure to 11km'] = 'p_0_11k = p_0*Pow((t/T_0),(-grav_acc/lambda_1/gas_constant))'
num_vars['Pressure to 11km'] = 7
equations['Pressure to 11km'] = Pressure_to_11km
# 
# 
# 
def Pressure_at_11km(solv_vars, vars, dict_val):
	grav_acc = vars[0]
	gas_constant = vars[1]
	lambda_1 = vars[2]
	T_0 = vars[3]
	T_11k = vars[4]
	p_0 = vars[5]
	p_11k = vars[6]

	eq = Eq(p_11k, p_0*Pow((T_11k/T_0),(-grav_acc/lambda_1/gas_constant)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Pressure at 11km')
vars_names['Pressure at 11km'] = ['Gravitational acceleration', 'Gas Constant', 'lambda_1', 'Temp at 0m', 'Temp at 11km', 'Pressure at 0m', 'Pressure at 11km']
variables['Pressure at 11km'] = ['grav_acc', 'gas_constant', 'lambda_1', 'T_0', 'T_11k', 'p_0', 'p_11k']
formulas['Pressure at 11km'] = 'p_11k = p_0*Pow((T_11k/T_0),(-grav_acc/lambda_1/gas_constant))'
num_vars['Pressure at 11km'] = 7
equations['Pressure at 11km'] = Pressure_at_11km
# 
# 
# 
def Pressure_to_20km(solv_vars, vars, dict_val):
	h = vars[0]
	grav_acc = vars[1]
	gas_constant = vars[2]
	T_11k = vars[3]
	p_11k = vars[4]
	p_11_20k = vars[5]

	eq = Eq(p_11_20k, p_11k*exp(-grav_acc*(h-11000)/(gas_constant*T_11k)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Pressure to 20km')
vars_names['Pressure to 20km'] = ['Altitude', 'Gravitational acceleration', 'Gas Constant', 'Temp at 11km', 'Pressure at 11km', 'Pressure to 20km']
variables['Pressure to 20km'] = ['h', 'grav_acc', 'gas_constant', 'T_11k', 'p_11k', 'p_11_20k']
formulas['Pressure to 20km'] = 'p_11_20k = p_11k*exp(-grav_acc*(h-11000)/(gas_constant*T_11k))'
num_vars['Pressure to 20km'] = 6
equations['Pressure to 20km'] = Pressure_to_20km
# 
# 
# 
def Pressure_at_20km(solv_vars, vars, dict_val):
	grav_acc = vars[0]
	gas_constant = vars[1]
	T_11k = vars[2]
	p_11k = vars[3]
	p_20k = vars[4]

	eq = Eq(p_20k, p_11k*exp(-grav_acc*(20000.0-11000.0)/(gas_constant*T_11k)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Pressure at 20km')
vars_names['Pressure at 20km'] = ['Gravitational acceleration', 'Gas Constant', 'Temp at 11km', 'Pressure at 11km', 'Pressure at 20km']
variables['Pressure at 20km'] = ['grav_acc', 'gas_constant', 'T_11k', 'p_11k', 'p_20k']
formulas['Pressure at 20km'] = 'p_20k = p_11k*exp(-grav_acc*(20000.0-11000.0)/(gas_constant*T_11k))'
num_vars['Pressure at 20km'] = 5
equations['Pressure at 20km'] = Pressure_at_20km
# 
# 
# 
def Pressure_to_32km(solv_vars, vars, dict_val):
	t = vars[0]
	grav_acc = vars[1]
	gas_constant = vars[2]
	lambda_3 = vars[3]
	T_20k = vars[4]
	p_20k = vars[5]
	p_20_32k = vars[6]

	eq = Eq(p_20_32k, p_20k*Pow((t/T_20k),(-grav_acc/lambda_3/gas_constant)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Pressure to 32km')
vars_names['Pressure to 32km'] = ['Temperatue', 'Gravitational acceleration', 'Gas Constant', 'lambda_3', 'Temp at 20km', 'Pressure at 20km', 'Pressure to 32km']
variables['Pressure to 32km'] = ['t', 'grav_acc', 'gas_constant', 'lambda_3', 'T_20k', 'p_20k', 'p_20_32k']
formulas['Pressure to 32km'] = 'p_20_32k = p_20k*Pow((t/T_20k),(-grav_acc/lambda_3/gas_constant))'
num_vars['Pressure to 32km'] = 7
equations['Pressure to 32km'] = Pressure_to_32km
# 
# 
# 
def Density_to_11km(solv_vars, vars, dict_val):
	t = vars[0]
	grav_acc = vars[1]
	gas_constant = vars[2]
	lambda_1 = vars[3]
	T_0 = vars[4]
	rho_0 = vars[5]
	rho_0_11k = vars[6]

	eq = Eq(rho_0_11k, rho_0*Pow((t/T_0),((-grav_acc/lambda_1/gas_constant)-1)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Density to 11km')
vars_names['Density to 11km'] = ['Temperatue', 'Gravitational acceleration', 'Gas Constant', 'lambda_1', 'Temp at 0m', 'Density at 0m', 'Density to 11km']
variables['Density to 11km'] = ['t', 'grav_acc', 'gas_constant', 'lambda_1', 'T_0', 'rho_0', 'rho_0_11k']
formulas['Density to 11km'] = 'rho_0_11k = rho_0*Pow((t/T_0),((-grav_acc/lambda_1/gas_constant)-1))'
num_vars['Density to 11km'] = 7
equations['Density to 11km'] = Density_to_11km
# 
# 
# 
def Density_at_11km(solv_vars, vars, dict_val):
	gas_constant = vars[0]
	T_11k = vars[1]
	p_11k = vars[2]
	rho_11k = vars[3]

	eq = Eq(rho_11k, p_11k/(T_11k*gas_constant))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Density at 11km')
vars_names['Density at 11km'] = ['Gas Constant', 'Temp at 11km', 'Pressure at 11km', 'Density at 11km']
variables['Density at 11km'] = ['gas_constant', 'T_11k', 'p_11k', 'rho_11k']
formulas['Density at 11km'] = 'rho_11k = p_11k/(T_11k*gas_constant)'
num_vars['Density at 11km'] = 4
equations['Density at 11km'] = Density_at_11km
# 
# 
# 
def Density_to_20km(solv_vars, vars, dict_val):
	h = vars[0]
	grav_acc = vars[1]
	gas_constant = vars[2]
	T_11k = vars[3]
	rho_11k = vars[4]
	rho_11_20k = vars[5]

	eq = Eq(rho_11_20k, rho_11k*exp(-grav_acc*(h-11000)/(gas_constant*T_11k)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Density to 20km')
vars_names['Density to 20km'] = ['Altitude', 'Gravitational acceleration', 'Gas Constant', 'Temp at 11km', 'Density at 11km', 'Density to 20km']
variables['Density to 20km'] = ['h', 'grav_acc', 'gas_constant', 'T_11k', 'rho_11k', 'rho_11_20k']
formulas['Density to 20km'] = 'rho_11_20k = rho_11k*exp(-grav_acc*(h-11000)/(gas_constant*T_11k))'
num_vars['Density to 20km'] = 6
equations['Density to 20km'] = Density_to_20km
# 
# 
# 
def Density_at_20km(solv_vars, vars, dict_val):
	gas_constant = vars[0]
	T_20k = vars[1]
	p_20k = vars[2]
	rho_20k = vars[3]

	eq = Eq(rho_20k, p_20k/(T_20k*gas_constant))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Density at 20km')
vars_names['Density at 20km'] = ['Gas Constant', 'Temp at 20km', 'Pressure at 20km', 'Density at 20km']
variables['Density at 20km'] = ['gas_constant', 'T_20k', 'p_20k', 'rho_20k']
formulas['Density at 20km'] = 'rho_20k = p_20k/(T_20k*gas_constant)'
num_vars['Density at 20km'] = 4
equations['Density at 20km'] = Density_at_20km
# 
# 
# 
def Density_to_32km(solv_vars, vars, dict_val):
	t = vars[0]
	grav_acc = vars[1]
	gas_constant = vars[2]
	lambda_3 = vars[3]
	T_20k = vars[4]
	rho_20k = vars[5]
	rho_20_32k = vars[6]

	eq = Eq(rho_20_32k, rho_20k*Pow((t/T_20k),(-grav_acc/lambda_3/gas_constant)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Density to 32km')
vars_names['Density to 32km'] = ['Temperatue', 'Gravitational acceleration', 'Gas Constant', 'lambda_3', 'Temp at 20km', 'Density at 20km', 'Density to 32km']
variables['Density to 32km'] = ['t', 'grav_acc', 'gas_constant', 'lambda_3', 'T_20k', 'rho_20k', 'rho_20_32k']
formulas['Density to 32km'] = 'rho_20_32k = rho_20k*Pow((t/T_20k),(-grav_acc/lambda_3/gas_constant))'
num_vars['Density to 32km'] = 7
equations['Density to 32km'] = Density_to_32km
# 
# 
# 
def Viscosity(solv_vars, vars, dict_val):
	t = vars[0]
	Sutherland_constant = vars[1]
	reference_temperature = vars[2]
	ref_visc = vars[3]
	miu = vars[4]

	eq = Eq(miu, ref_visc*(reference_temperature+Sutherland_constant)/(t+Sutherland_constant)*Pow((t/reference_temperature),(3.0/2.0)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Viscosity')
vars_names['Viscosity'] = ['Temperatue', 'Sutherland Constant', 'Reference Temperature', 'Reference Viscosity', 'Viscosity']
variables['Viscosity'] = ['t', 'Sutherland_constant', 'reference_temperature', 'ref_visc', 'miu']
formulas['Viscosity'] = 'miu = ref_visc*(reference_temperature+Sutherland_constant)/(t+Sutherland_constant)*Pow((t/reference_temperature),(3.0/2.0))'
num_vars['Viscosity'] = 5
equations['Viscosity'] = Viscosity
# 
# 
# 
def Speed_of_sound(solv_vars, vars, dict_val):
	t = vars[0]
	gas_constant = vars[1]
	specific_heat_ratio = vars[2]
	a = vars[3]

	eq = Eq(a, sqrt(specific_heat_ratio*gas_constant*t))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Speed of sound')
vars_names['Speed of sound'] = ['Temperatue', 'Gas Constant', 'Specific Heat Ratio', 'Speed of sound']
variables['Speed of sound'] = ['t', 'gas_constant', 'specific_heat_ratio', 'a']
formulas['Speed of sound'] = 'a = sqrt(specific_heat_ratio*gas_constant*t)'
num_vars['Speed of sound'] = 4
equations['Speed of sound'] = Speed_of_sound
# 
# 
# 