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
def natural_frequency(solv_vars, vars, dict_val):
	omega_n = vars[0]
	k = vars[1]
	m = vars[2]

	eq = Eq(omega_n, sqrt(k/m))
	result = solve(eq, solv_vars[0], dict=dict_val)

	return result

name = "Natural Frequency"
names.append(name)
vars_names[name] = ["Nat Freq", "Stiffness", "Mass"]
variables[name] = ["omega_n", "k", "m"]
formulas[name] = "omega_n = sqrt(k/m)"
num_vars[name] = 3
equations[name] = natural_frequency
# 
# 
# 
def Damping_Ratio(solv_vars, vars, dict_val):
	zeta = vars[0]
	c = vars[1]
	c_cr = vars[2]

	eq = Eq(zeta, c / c_cr)
	result = solve(eq, solv_vars[0], dict=dict_val)

	return result

name = "Damping Ratio"
names.append("Damping Ratio")
vars_names["Damping Ratio"] = ["zeta", "Damping", "Damping Cr"]
variables["Damping Ratio"] = ["zeta", "c", "c_cr"]
formulas["Damping Ratio"] = "zeta = c / c_cr"
num_vars["Damping Ratio"] = 3
equations["Damping Ratio"] = Damping_Ratio
# 
# 
# 		
def Critical_Damping(solv_vars, vars, dict_val):
	c_cr = vars[0]
	k = vars[1]
	m = vars[2]
	#omega_n

	eq = Eq(c_cr, 2 * sqrt(k * m))
	#eq = Eq(c_cr, 2 * omega_n * m))
	result = solve(eq, solv_vars[0], dict=dict_val)

	return result

name = "Critical Damping"
names.append("Critical Damping")
vars_names["Critical Damping"] = ["Damping C", "Stiffness", "Mass"]
variables["Critical Damping"] = ["c_cr", "k", "m"]
formulas["Critical Damping"] = "c_cr = 2 * sqrt(k * m)"
num_vars["Critical Damping"] = 3
equations["Critical Damping"] = Critical_Damping
# 
# 
# 
def Octaves(solv_vars, vars, dict_val):
	octave = vars[0]
	f_L = vars[1]
	f_H = vars[2]
	
	eq = Eq(octave, log(f_H/f_L) / log(2))
	
	result = solve(eq, solv_vars[0], dict=dict_val)

	return result

name = "Octaves"
names.append(name)
vars_names["Octaves"] = ["Octaves", "Low Frequency", "High Frequency"]
variables["Octaves"] = ["oct", "f_L", "f_H"]
formulas["Octaves"] = "oct = log(f_H/f_L) / log(2)"
num_vars["Octaves"] = 3
equations["Octaves"] = Octaves
# 
# 
# 
def DeciBell(solv_vars, vars, dict_val):
	decibell = vars[0]
	ASD_L = vars[1]
	ASD_H = vars[2]
	
	eq = Eq(decibell, 10 * log(ASD_H/ASD_L))
	
	result = solve(eq, solv_vars[0], dict=dict_val)

	return result

name = "Octaves"
names.append("DeciBell")
vars_names["DeciBell"] = ["DeciBell", "Low Frequency", "High Frequency"]
variables["DeciBell"] = ["dB", "ASD_L", "ASD_H"]
formulas["DeciBell"] = "dB = 10 * log(ASD_H/ASD_L)"
num_vars["DeciBell"] = 3
equations["DeciBell"] = DeciBell
# 
# 
# 
def DeciBell_Octave(solv_vars, vars, dict_val):
	db_oct = vars[0]
	db = vars[1]
	oct = vars[2]
	
	eq = Eq(db_oct, db/oct)
	
	result = solve(eq, solv_vars[0], dict=dict_val)

	return result

name = "Octaves"
names.append("DeciBell Octave")
vars_names["DeciBell Octave"] = ["DeciBell per Octave", "DeciBell", "Octave"]
variables["DeciBell Octave"] = ["dB_oct", "dB", "oct"]
formulas["DeciBell Octave"] = "dB_oct = dB/oct"
num_vars["DeciBell Octave"] = 3
equations["DeciBell Octave"] = DeciBell_Octave
# 
# 
# 	