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
# 
# 
# 
def Intake_Pressure(solv_vars, vars, dict_val):
	C_a = vars[0]
	T_a = vars[1]
	cp_a = vars[2]
	eta_i = vars[3]
	gamma_a = vars[4]
	p_a = vars[5]
	p_intake = vars[6]

	eq = Eq(p_intake, p_a*(1+eta_i*(C_a**2/(2*cp_a*T_a)))**(gamma_a/(gamma_a-1)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Intake Pressure')
vars_names['Intake Pressure'] = ['Aircraft Speed', 'Admission Temperature', 'Fresh air SHC', 'Intake Isentropic Efficiency', 'Fresh Air SHC ratio', 'Admission Pressure', 'Aft Intake Pressure']
variables['Intake Pressure'] = ['C_a', 'T_a', 'cp_a', 'eta_i', 'gamma_a', 'p_a', 'p_intake']
formulas['Intake Pressure'] = 'p_intake = p_a*(1+eta_i*(C_a**2/(2*cp_a*T_a)))**(gamma_a/(gamma_a-1))'
num_vars['Intake Pressure'] = 7
equations['Intake Pressure'] = Intake_Pressure
# 
# 
# 
def Fan_Temperature(solv_vars, vars, dict_val):
	T_fan = vars[0]
	T_intake = vars[1]
	eta_fan = vars[2]
	fpr = vars[3]
	gamma_a = vars[4]

	eq = Eq(T_fan, T_intake+T_intake/eta_fan*(fpr**((gamma_a-1)/gamma_a)-1))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Fan Temperature')
vars_names['Fan Temperature'] = ['Aft Fan Temperature', 'Aft Intake Temperature', 'Fan Isentropic Efficiency', 'Fan Pressure Ratio', 'Fresh Air SHC ratio']
variables['Fan Temperature'] = ['T_fan', 'T_intake', 'eta_fan', 'fpr', 'gamma_a']
formulas['Fan Temperature'] = 'T_fan = T_intake+T_intake/eta_fan*(fpr**((gamma_a-1)/gamma_a)-1)'
num_vars['Fan Temperature'] = 5
equations['Fan Temperature'] = Fan_Temperature
# 
# 
# 
def Fan_Pressure(solv_vars, vars, dict_val):
	fpr = vars[0]
	p_fan = vars[1]
	p_intake = vars[2]

	eq = Eq(p_fan, fpr*p_intake)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Fan Pressure')
vars_names['Fan Pressure'] = ['Fan Pressure Ratio', 'Aft Fan Pressure', 'Aft Intake Pressure']
variables['Fan Pressure'] = ['fpr', 'p_fan', 'p_intake']
formulas['Fan Pressure'] = 'p_fan = fpr*p_intake'
num_vars['Fan Pressure'] = 3
equations['Fan Pressure'] = Fan_Pressure
# 
# 
# 
def Compression_Temperature(solv_vars, vars, dict_val):
	T_compression = vars[0]
	T_intake = vars[1]
	cr = vars[2]
	eta_c = vars[3]
	gamma_a = vars[4]

	eq = Eq(T_compression, T_intake+T_intake/eta_c*(cr**((gamma_a-1)/gamma_a)-1))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Compression Temperature')
vars_names['Compression Temperature'] = ['Aft Compression Temperature', 'Aft Intake Temperature', 'Compressor Ratio', 'Compressor Isentropic Efficiency', 'Fresh Air SHC ratio']
variables['Compression Temperature'] = ['T_compression', 'T_intake', 'cr', 'eta_c', 'gamma_a']
formulas['Compression Temperature'] = 'T_compression = T_intake+T_intake/eta_c*(cr**((gamma_a-1)/gamma_a)-1)'
num_vars['Compression Temperature'] = 5
equations['Compression Temperature'] = Compression_Temperature
# 
# 
# 
def Compression_Pressure(solv_vars, vars, dict_val):
	cr = vars[0]
	p_compression = vars[1]
	p_intake = vars[2]

	eq = Eq(p_compression, cr*p_intake)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Compression Pressure')
vars_names['Compression Pressure'] = ['Compressor Ratio', 'Aft Compression Pressure', 'Aft Intake Pressure']
variables['Compression Pressure'] = ['cr', 'p_compression', 'p_intake']
formulas['Compression Pressure'] = 'p_compression = cr*p_intake'
num_vars['Compression Pressure'] = 3
equations['Compression Pressure'] = Compression_Pressure
# 
# 
# 
def Combustion_Temperature(solv_vars, vars, dict_val):
	T_combustion = vars[0]

	eq = Eq(T_combustion, T_combustion)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Combustion Temperature')
vars_names['Combustion Temperature'] = ['Aft Combustion Temperature']
variables['Combustion Temperature'] = ['T_combustion']
formulas['Combustion Temperature'] = 'T_combustion = T_combustion'
num_vars['Combustion Temperature'] = 1
equations['Combustion Temperature'] = Combustion_Temperature
# 
# 
# 
def Combustion_Pressure(solv_vars, vars, dict_val):
	delta_p_b = vars[0]
	p_combustion = vars[1]
	p_compression = vars[2]

	eq = Eq(p_combustion, p_compression*(1-delta_p_b/100))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Combustion Pressure')
vars_names['Combustion Pressure'] = ['Pressure Drop In Combustion Chamber', 'Aft Combustion Pressure', 'Aft Compression Pressure']
variables['Combustion Pressure'] = ['delta_p_b', 'p_combustion', 'p_compression']
formulas['Combustion Pressure'] = 'p_combustion = p_compression*(1-delta_p_b/100)'
num_vars['Combustion Pressure'] = 3
equations['Combustion Pressure'] = Combustion_Pressure
# 
# 
# 
def Expansion_Temperature(solv_vars, vars, dict_val):
	T_combustion = vars[0]
	T_compression = vars[1]
	T_expansion = vars[2]
	T_intake = vars[3]
	cp_a = vars[4]
	cp_g = vars[5]
	eta_transmission = vars[6]

	eq = Eq(T_expansion, T_combustion-(eta_transmission*cp_a*(T_compression-T_intake)/cp_g))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Expansion Temperature')
vars_names['Expansion Temperature'] = ['Aft Combustion Temperature', 'Aft Compression Temperature', 'Aft Expansion Temperature', 'Aft Intake Temperature', 'Fresh air SHC', 'Burned gas SHC', 'Transmission Efficiency']
variables['Expansion Temperature'] = ['T_combustion', 'T_compression', 'T_expansion', 'T_intake', 'cp_a', 'cp_g', 'eta_transmission']
formulas['Expansion Temperature'] = 'T_expansion = T_combustion-(eta_transmission*cp_a*(T_compression-T_intake)/cp_g)'
num_vars['Expansion Temperature'] = 7
equations['Expansion Temperature'] = Expansion_Temperature
# 
# 
# 
def Expansion_Pressure(solv_vars, vars, dict_val):
	T_combustion = vars[0]
	T_expansion = vars[1]
	eta_t = vars[2]
	gamma_g = vars[3]
	p_combustion = vars[4]
	p_expansion = vars[5]

	eq = Eq(p_expansion, p_combustion*(1-(T_combustion-T_expansion)/(eta_t*T_combustion))**(gamma_g/(gamma_g-1)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Expansion Pressure')
vars_names['Expansion Pressure'] = ['Aft Combustion Temperature', 'Aft Expansion Temperature', 'Turbine Isentropic Efficiency', 'Burned Gas SHC ratio', 'Aft Combustion Pressure', 'Aft Expansion Pressure']
variables['Expansion Pressure'] = ['T_combustion', 'T_expansion', 'eta_t', 'gamma_g', 'p_combustion', 'p_expansion']
formulas['Expansion Pressure'] = 'p_expansion = p_combustion*(1-(T_combustion-T_expansion)/(eta_t*T_combustion))**(gamma_g/(gamma_g-1))'
num_vars['Expansion Pressure'] = 6
equations['Expansion Pressure'] = Expansion_Pressure
# 
# 
# 
def Compressor_Power(solv_vars, vars, dict_val):
	T_compression = vars[0]
	T_intake = vars[1]
	cp_a = vars[2]
	P_c = vars[3]

	eq = Eq(P_c, cp_a*(T_compression-T_intake))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Compressor Power')
vars_names['Compressor Power'] = ['Aft Compression Temperature', 'Aft Intake Temperature', 'Fresh air SHC', 'Compressor Power']
variables['Compressor Power'] = ['T_compression', 'T_intake', 'cp_a', 'P_c']
formulas['Compressor Power'] = 'P_c = cp_a*(T_compression-T_intake)'
num_vars['Compressor Power'] = 4
equations['Compressor Power'] = Compressor_Power
# 
# 
# 
def Turbine_Power(solv_vars, vars, dict_val):
	T_combustion = vars[0]
	T_expansion = vars[1]
	cp_g = vars[2]
	P_t = vars[3]

	eq = Eq(P_t, cp_g*(T_combustion-T_expansion))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbine Power')
vars_names['Turbine Power'] = ['Aft Combustion Temperature', 'Aft Expansion Temperature', 'Burned gas SHC', 'Turbine Power']
variables['Turbine Power'] = ['T_combustion', 'T_expansion', 'cp_g', 'P_t']
formulas['Turbine Power'] = 'P_t = cp_g*(T_combustion-T_expansion)'
num_vars['Turbine Power'] = 4
equations['Turbine Power'] = Turbine_Power
# 
# 
# 
def Compressor_Power_tfa(solv_vars, vars, dict_val):
	T_compression = vars[0]
	T_intake = vars[1]
	cp_a = vars[2]
	m_h = vars[3]
	P_c_tfa = vars[4]

	eq = Eq(P_c_tfa, m_h*cp_a*(T_compression-T_intake))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Compressor Power tfa')
vars_names['Compressor Power tfa'] = ['Aft Compression Temperature', 'Aft Intake Temperature', 'Fresh air SHC', 'Hot Massic Flow Rate', 'Compressor Power tfa']
variables['Compressor Power tfa'] = ['T_compression', 'T_intake', 'cp_a', 'm_h', 'P_c_tfa']
formulas['Compressor Power tfa'] = 'P_c_tfa = m_h*cp_a*(T_compression-T_intake)'
num_vars['Compressor Power tfa'] = 5
equations['Compressor Power tfa'] = Compressor_Power_tfa
# 
# 
# 
def Turbine_Power_tfa(solv_vars, vars, dict_val):
	T_combustion = vars[0]
	T_expansion = vars[1]
	cp_g = vars[2]
	m_h = vars[3]
	P_t_tfa = vars[4]

	eq = Eq(P_t_tfa, m_h*cp_g*(T_combustion-T_expansion))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Turbine Power tfa')
vars_names['Turbine Power tfa'] = ['Aft Combustion Temperature', 'Aft Expansion Temperature', 'Burned gas SHC', 'Hot Massic Flow Rate', 'Turbine Power tfa']
variables['Turbine Power tfa'] = ['T_combustion', 'T_expansion', 'cp_g', 'm_h', 'P_t_tfa']
formulas['Turbine Power tfa'] = 'P_t_tfa = m_h*cp_g*(T_combustion-T_expansion)'
num_vars['Turbine Power tfa'] = 5
equations['Turbine Power tfa'] = Turbine_Power_tfa
# 
# 
# 
def Compressor_Power_Other(solv_vars, vars, dict_val):
	eta_transmission = vars[0]
	P_c_other = vars[1]
	P_t = vars[2]

	eq = Eq(P_c_other, P_t/eta_transmission)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Compressor Power Other')
vars_names['Compressor Power Other'] = ['Transmission Efficiency', 'Compressor Power Other', 'Turbine Power']
variables['Compressor Power Other'] = ['eta_transmission', 'P_c_other', 'P_t']
formulas['Compressor Power Other'] = 'P_c_other = P_t/eta_transmission'
num_vars['Compressor Power Other'] = 3
equations['Compressor Power Other'] = Compressor_Power_Other
# 
# 
# 
def Critic_Pressures_Ratio(solv_vars, vars, dict_val):
	eta_j = vars[0]
	gamma_g = vars[1]
	r_p_c = vars[2]

	eq = Eq(r_p_c, 1/(1-1/eta_j*((gamma_g-1)/(gamma_g+1)))**(gamma_g/(gamma_g-1)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Critic Pressures Ratio')
vars_names['Critic Pressures Ratio'] = ['Jet Isentropic Efficiency', 'Burned Gas SHC ratio', 'Critic Pressures ratio']
variables['Critic Pressures Ratio'] = ['eta_j', 'gamma_g', 'r_p_c']
formulas['Critic Pressures Ratio'] = 'r_p_c = 1/(1-1/eta_j*((gamma_g-1)/(gamma_g+1)))**(gamma_g/(gamma_g-1))'
num_vars['Critic Pressures Ratio'] = 3
equations['Critic Pressures Ratio'] = Critic_Pressures_Ratio
# 
# 
# 
def Pressures_Ratio(solv_vars, vars, dict_val):
	p_a = vars[0]
	p_expansion = vars[1]
	r_p_a = vars[2]

	eq = Eq(r_p_a, p_expansion/p_a)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Pressures Ratio')
vars_names['Pressures Ratio'] = ['Admission Pressure', 'Aft Expansion Pressure', 'Pressures Ratio']
variables['Pressures Ratio'] = ['p_a', 'p_expansion', 'r_p_a']
formulas['Pressures Ratio'] = 'r_p_a = p_expansion/p_a'
num_vars['Pressures Ratio'] = 3
equations['Pressures Ratio'] = Pressures_Ratio
# 
# 
# 
def Choking_Pressure(solv_vars, vars, dict_val):
	p_exhaust_choking = vars[0]
	p_expansion = vars[1]
	r_p_c = vars[2]

	eq = Eq(p_exhaust_choking, p_expansion/r_p_c)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Choking Pressure')
vars_names['Choking Pressure'] = ['Choking Pressure', 'Aft Expansion Pressure', 'Critic Pressures ratio']
variables['Choking Pressure'] = ['p_exhaust_choking', 'p_expansion', 'r_p_c']
formulas['Choking Pressure'] = 'p_exhaust_choking = p_expansion/r_p_c'
num_vars['Choking Pressure'] = 3
equations['Choking Pressure'] = Choking_Pressure
# 
# 
# 
def Choking_Temperature(solv_vars, vars, dict_val):
	T_exhaust_choking = vars[0]
	T_expansion = vars[1]
	gamma_g = vars[2]

	eq = Eq(T_exhaust_choking, (2*T_expansion)/(gamma_g+1))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Choking Temperature')
vars_names['Choking Temperature'] = ['Choking Temperature', 'Aft Expansion Temperature', 'Burned Gas SHC ratio']
variables['Choking Temperature'] = ['T_exhaust_choking', 'T_expansion', 'gamma_g']
formulas['Choking Temperature'] = 'T_exhaust_choking = (2*T_expansion)/(gamma_g+1)'
num_vars['Choking Temperature'] = 3
equations['Choking Temperature'] = Choking_Temperature
# 
# 
# 
def Choking_Speed(solv_vars, vars, dict_val):
	C_exhaust_choking = vars[0]
	T_expansion = vars[1]
	gamma_g = vars[2]
	gas_cnt = vars[3]

	eq = Eq(C_exhaust_choking, sqrt(gamma_g*gas_cnt*T_expansion))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Choking Speed')
vars_names['Choking Speed'] = ['Choking', 'Aft Expansion Temperature', 'Burned Gas SHC ratio', 'Gas Constant']
variables['Choking Speed'] = ['C_exhaust_choking', 'T_expansion', 'gamma_g', 'gas_cnt']
formulas['Choking Speed'] = 'C_exhaust_choking = sqrt(gamma_g*gas_cnt*T_expansion)'
num_vars['Choking Speed'] = 4
equations['Choking Speed'] = Choking_Speed
# 
# 
# 
def Choking_Density(solv_vars, vars, dict_val):
	T_expansion = vars[0]
	gas_cnt = vars[1]
	p_exhaust_choking = vars[2]
	rho_exhaust_choking = vars[3]

	eq = Eq(rho_exhaust_choking, (p_exhaust_choking*10**5)/(gas_cnt*T_expansion))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Choking Density')
vars_names['Choking Density'] = ['Aft Expansion Temperature', 'Gas Constant', 'Choking Pressure', 'Choking Density']
variables['Choking Density'] = ['T_expansion', 'gas_cnt', 'p_exhaust_choking', 'rho_exhaust_choking']
formulas['Choking Density'] = 'rho_exhaust_choking = (p_exhaust_choking*10**5)/(gas_cnt*T_expansion)'
num_vars['Choking Density'] = 4
equations['Choking Density'] = Choking_Density
# 
# 
# 
def No_Choking_Pressure(solv_vars, vars, dict_val):
	p_a = vars[0]
	p_exhaust_no_choking = vars[1]

	eq = Eq(p_exhaust_no_choking, p_a)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('No Choking Pressure')
vars_names['No Choking Pressure'] = ['Admission Pressure', 'No Choking Pressure']
variables['No Choking Pressure'] = ['p_a', 'p_exhaust_no_choking']
formulas['No Choking Pressure'] = 'p_exhaust_no_choking = p_a'
num_vars['No Choking Pressure'] = 2
equations['No Choking Pressure'] = No_Choking_Pressure
# 
# 
# 
def No_Choking_Temperature(solv_vars, vars, dict_val):
	T_exhaust_no_choking = vars[0]
	T_expansion = vars[1]
	eta_j = vars[2]
	gamma_g = vars[3]
	p_exhaust_no_choking = vars[4]
	p_expansion = vars[5]

	eq = Eq(T_exhaust_no_choking, T_expansion-eta_j*T_expansion*(1-(p_exhaust_no_choking/p_expansion)**((gamma_g-1)/gamma_g)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('No Choking Temperature')
vars_names['No Choking Temperature'] = ['No Choking Temperature', 'Aft Expansion Temperature', 'Jet Isentropic Efficiency', 'Burned Gas SHC ratio', 'No Choking Pressure', 'Aft Expansion Pressure']
variables['No Choking Temperature'] = ['T_exhaust_no_choking', 'T_expansion', 'eta_j', 'gamma_g', 'p_exhaust_no_choking', 'p_expansion']
formulas['No Choking Temperature'] = 'T_exhaust_no_choking = T_expansion-eta_j*T_expansion*(1-(p_exhaust_no_choking/p_expansion)**((gamma_g-1)/gamma_g))'
num_vars['No Choking Temperature'] = 6
equations['No Choking Temperature'] = No_Choking_Temperature
# 
# 
# 
def No_Choking_Speed(solv_vars, vars, dict_val):
	C_exhaust_no_choking = vars[0]
	T_expansion = vars[1]
	cp_g = vars[2]

	eq = Eq(C_exhaust_no_choking, sqrt(2*cp_g*(T_expansion-T_expansion)))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('No Choking Speed')
vars_names['No Choking Speed'] = ['No Choking', 'Aft Expansion Temperature', 'Burned gas SHC']
variables['No Choking Speed'] = ['C_exhaust_no_choking', 'T_expansion', 'cp_g']
formulas['No Choking Speed'] = 'C_exhaust_no_choking = sqrt(2*cp_g*(T_expansion-T_expansion))'
num_vars['No Choking Speed'] = 3
equations['No Choking Speed'] = No_Choking_Speed
# 
# 
# 
def No_Choking_Density(solv_vars, vars, dict_val):
	T_expansion = vars[0]
	gas_cnt = vars[1]
	p_exhaust_no_choking = vars[2]
	rho_exhaust_no_choking = vars[3]

	eq = Eq(rho_exhaust_no_choking, (p_exhaust_no_choking*10**5)/(gas_cnt*T_expansion))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('No Choking Density')
vars_names['No Choking Density'] = ['Aft Expansion Temperature', 'Gas Constant', 'No Choking Pressure', 'No Choking Density']
variables['No Choking Density'] = ['T_expansion', 'gas_cnt', 'p_exhaust_no_choking', 'rho_exhaust_no_choking']
formulas['No Choking Density'] = 'rho_exhaust_no_choking = (p_exhaust_no_choking*10**5)/(gas_cnt*T_expansion)'
num_vars['No Choking Density'] = 4
equations['No Choking Density'] = No_Choking_Density
# 
# 
# 
def Fuel_Air_Ratio_Efficiency(solv_vars, vars, dict_val):
	eta_b = vars[0]
	f = vars[1]
	f_line = vars[2]

	eq = Eq(f_line, f/eta_b)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Fuel Air Ratio Efficiency')
vars_names['Fuel Air Ratio Efficiency'] = ['Combustion Efficiency', 'Fuel Air Ratio', 'Fuel Air Ratio times eta_b']
variables['Fuel Air Ratio Efficiency'] = ['eta_b', 'f', 'f_line']
formulas['Fuel Air Ratio Efficiency'] = 'f_line = f/eta_b'
num_vars['Fuel Air Ratio Efficiency'] = 3
equations['Fuel Air Ratio Efficiency'] = Fuel_Air_Ratio_Efficiency
# 
# 
# 
def Jet_Nozzle_Area(solv_vars, vars, dict_val):
	A_j = vars[0]
	C_j = vars[1]
	m_a = vars[2]
	rho_j = vars[3]

	eq = Eq(A_j, m_a/(rho_j*C_j))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Jet Nozzle Area')
vars_names['Jet Nozzle Area'] = ['Jet Nozzle Area', 'Jet Speed', 'Intake Massic Flow Rate', 'unknow']
variables['Jet Nozzle Area'] = ['A_j', 'C_j', 'm_a', 'rho_j']
formulas['Jet Nozzle Area'] = 'A_j = m_a/(rho_j*C_j)'
num_vars['Jet Nozzle Area'] = 4
equations['Jet Nozzle Area'] = Jet_Nozzle_Area
# 
# 
# 
def Thrust(solv_vars, vars, dict_val):
	A_j = vars[0]
	C_a = vars[1]
	C_j = vars[2]
	m_a = vars[3]
	p_a = vars[4]
	p_j = vars[5]
	thrust = vars[6]

	eq = Eq(thrust, m_a*(C_j-C_a)+A_j*(p_j-p_a))

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Thrust')
vars_names['Thrust'] = ['Jet Nozzle Area', 'Aircraft Speed', 'Jet Speed', 'Intake Massic Flow Rate', 'Admission Pressure', 'Jet Pressure', 'Thrust']
variables['Thrust'] = ['A_j', 'C_a', 'C_j', 'm_a', 'p_a', 'p_j', 'thrust']
formulas['Thrust'] = 'thrust = m_a*(C_j-C_a)+A_j*(p_j-p_a)'
num_vars['Thrust'] = 7
equations['Thrust'] = Thrust
# 
# 
# 
def Specific_Thrust(solv_vars, vars, dict_val):
	m_a = vars[0]
	thrust = vars[1]
	thrust_s = vars[2]

	eq = Eq(thrust_s, thrust/m_a)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Specific Thrust')
vars_names['Specific Thrust'] = ['Intake Massic Flow Rate', 'Thrust', 'Specific thrust']
variables['Specific Thrust'] = ['m_a', 'thrust', 'thrust_s']
formulas['Specific Thrust'] = 'thrust_s = thrust/m_a'
num_vars['Specific Thrust'] = 3
equations['Specific Thrust'] = Specific_Thrust
# 
# 
# 
def Fuel_Flow(solv_vars, vars, dict_val):
	f_line = vars[0]
	m_a = vars[1]
	m_f = vars[2]

	eq = Eq(m_f, f_line*m_a)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Fuel Flow')
vars_names['Fuel Flow'] = ['Fuel Air Ratio times eta_b', 'Intake Massic Flow Rate', 'Fuel Massic Flow']
variables['Fuel Flow'] = ['f_line', 'm_a', 'm_f']
formulas['Fuel Flow'] = 'm_f = f_line*m_a'
num_vars['Fuel Flow'] = 3
equations['Fuel Flow'] = Fuel_Flow
# 
# 
# 
def Thrust_Specific_Fuel_Consumption(solv_vars, vars, dict_val):
	TSFC = vars[0]
	m_f = vars[1]
	thrust = vars[2]

	eq = Eq(TSFC, 3600*m_f/thrust)

	results = solve(eq, solv_vars[0], dict = dict_val)

	return results

names.append('Thrust Specific Fuel Consumption')
vars_names['Thrust Specific Fuel Consumption'] = ['Thrust Specific Fuel Consumpion', 'Fuel Massic Flow', 'Thrust']
variables['Thrust Specific Fuel Consumption'] = ['TSFC', 'm_f', 'thrust']
formulas['Thrust Specific Fuel Consumption'] = 'TSFC = 3600*m_f/thrust'
num_vars['Thrust Specific Fuel Consumption'] = 3
equations['Thrust Specific Fuel Consumption'] = Thrust_Specific_Fuel_Consumption
# 
# 
# 
