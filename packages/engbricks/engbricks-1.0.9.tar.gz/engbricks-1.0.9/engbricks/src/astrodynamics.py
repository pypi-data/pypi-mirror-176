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
latex_formulas = {}
# 
# 
# 
def semi_major_axis(solv_vars, vars, dict_val):
    a = vars[0]
    r_a = vars[1]
    r_p = vars[2]

    eq = Eq(a, (r_a + r_p) / 2)
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Semi Major Axis"
names.append(name)
vars_names["Semi Major Axis"] = ["Semi Major Axis", "Apogee Radius", "Perigee Radius"]
variables["Semi Major Axis"] = ["a", "r_a", "r_p"]
formulas["Semi Major Axis"] = "a = (r_a + r_p) / 2"
num_vars["Semi Major Axis"] = 3
equations["Semi Major Axis"] = semi_major_axis
latex_formulas[name] = ""
# 
# 
# 
def semi_minor_axis(solv_vars, vars, dict_val):
    b = vars[0]
    r_a = vars[1]
    r_p = vars[2]

    eq = Eq(b, sqrt(r_a * r_p))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Semi Minor Axis"
names.append(name)
vars_names["Semi Minor Axis"] = ["Semi Minor Axis", "Apogee Radius", "Perigee Radius"]
variables["Semi Minor Axis"] = ["b", "r_a", "r_p"]
formulas["Semi Minor Axis"] = "b = sqrt(r_a * r_p)"
num_vars["Semi Minor Axis"] = 3
equations["Semi Minor Axis"] = semi_minor_axis
latex_formulas[name] = ""
# 
# 
# 
def apogee_radius(solv_vars, vars, dict_val):
    r_a = vars[0]
    p = vars[1]
    e = vars[2]

    eq = Eq(r_a, p/(1 - e))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Apogee Radius"
names.append(name)
vars_names["Apogee Radius"] = ["Apogee Radius", "Focal Parameter", "Eccentricity"]
variables["Apogee Radius"] = ["r_a", "p", "e"]
formulas["Apogee Radius"] = "r_a = p/(1 - e)"
num_vars["Apogee Radius"] = 3
equations["Apogee Radius"] = apogee_radius
latex_formulas[name] = ""
# 
# 
# 
def perigee_radius(solv_vars, vars, dict_val):
    r_p = vars[0]
    p = vars[1]
    e = vars[2]

    eq = Eq(r_p, p/(1 + e))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Perigee Radius"
names.append(name)
vars_names["Perigee Radius"] = ["Perigee Radius", "Focal Parameter", "Eccentricity"]
variables["Perigee Radius"] = ["r_p", "p", "e"]
formulas["Perigee Radius"] = "r_p = p/(1 + e)"
num_vars["Perigee Radius"] = 3
equations["Perigee Radius"] = perigee_radius
latex_formulas[name] = ""
# 
# 
# 
def orbital_radius(solv_vars, vars, dict_val):
    r = vars[0]
    p = vars[1]
    e = vars[2]
    theta = vars[3]

    eq = Eq(r, p / (1 + e * cos(theta)))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Orbital Radius"
names.append(name)
vars_names["Orbital Radius"] = ["Orbital Radius", "Focal Parameter", "Eccentricity" "Orbital Angle"]
variables["Orbital Radius"] = ["r", "p", "e", "theta"]
formulas["Orbital Radius"] = "r = p / (1 + e * cos(theta))"
num_vars["Orbital Radius"] = 4
equations["Orbital Radius"] = orbital_radius
latex_formulas[name] = ""
# 
# 
# 
def focal_parameter(solv_vars, vars, dict_val):
    p = vars[0]
    V_a = vars[1]
    r_a = vars[2]
    mu = vars[3]

    eq = Eq(p, (V_a**2 * r_a**2)/mu)
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Focal Parameter"
names.append(name)
vars_names["Focal Parameter"] = ["Focal Parameter", "Apogee Speed", "Apogee Radius", "Standard Gravitational Parameter"]
variables["Focal Parameter"] = ["p", "V_a", "r_a", "mu"]
formulas["Focal Parameter"] = "p = ((V_a**2 * r_a**2)/mu)"
num_vars["Focal Parameter"] = 4
equations["Focal Parameter"] = focal_parameter
latex_formulas[name] = ""
# 
# 
# 
def perigee_altitude(solv_vars, vars, dict_val):
    h_p = vars[0]
    r_p = vars[1]
    R = vars[2]

    eq = Eq(h_p, r_p + R)
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Perigee Altitude"
names.append(name)
vars_names["Perigee Altitude"] = ["Perigee Altitude", "Perigee Radius", "Main Body Radius"]
variables["Perigee Altitude"] = ["h_p", "r_p", "R"]
formulas["Perigee Altitude"] = "h_p = r_p + R"
num_vars["Perigee Altitude"] = 3
equations["Perigee Altitude"] = perigee_altitude
latex_formulas[name] = ""
# 
# 
# 
def apogee_altitude(solv_vars, vars, dict_val):
    h_a = vars[0]
    r_a = vars[1]
    R = vars[2]

    eq = Eq(h_a, r_a + R)
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Apogee Altitude"
names.append(name)
vars_names["Apogee Altitude"] = ["Apogee Altitude", "Apogee Radius", "Main Body Radius"]
variables["Apogee Altitude"] = ["h_a", "r_a", "R"]
formulas["Apogee Altitude"] = "h_a = r_a + R"
num_vars["Apogee Altitude"] = 3
equations["Apogee Altitude"] = apogee_altitude
latex_formulas[name] = ""
# 
# 
# 
def perigee_speed(solv_vars, vars, dict_val):
    V_p = vars[0]
    mu = vars[1]
    p = vars[2]
    e = vars[3]

    eq = Eq(V_p, sqrt(mu/p) * (1-e))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Perigee Speed"
names.append(name)
vars_names["Perigee Speed"] = ["Perigee Speed", "Standard Gravitational Parameter", "Focal Parameter", "Eccentricity"]
variables["Perigee Speed"] = ["V_p", "mu", "p", "e"]
formulas["Perigee Speed"] = "V_p = sqrt(mu/p) * (1 - e)"
num_vars["Perigee Speed"] = 4
equations["Perigee Speed"] = perigee_speed
latex_formulas[name] = ""
# 
# 
# 
def apogee_speed(solv_vars, vars, dict_val):
    V_a = vars[0]
    mu = vars[1]
    p = vars[2]
    e = vars[3]

    eq = Eq(V_a, sqrt(mu/p) * (1+e))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Apogee Speed"
names.append(name)
vars_names["Apogee Speed"] = ["Apogee Speed", "Standard Gravitational Parameter", "Focal Parameter", "Eccentricity"]
variables["Apogee Speed"] = ["V_a", "mu", "p", "e"]
formulas["Apogee Speed"] = "V_a = sqrt(mu/p) * (1+e)"
num_vars["Apogee Speed"] = 4
equations["Apogee Speed"] = apogee_speed
latex_formulas[name] = ""
# 
# 
# 
def orbital_speed(solv_vars, vars, dict_val):
    V = vars[0]
    mu = vars[1]
    r = vars[2]
    a = vars[3]

    eq = Eq(V, sqrt((2 * mu)/r - mu/a))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result
    
name = "Orbital Speed"
names.append(name)
vars_names["Orbital Speed"] = ["Orbital Speed", "Standard Gravitational Parameter", "Orbital Radius", "Semi Major Axis"]
variables["Orbital Speed"] = ["V", "mu", "r", "a"]
formulas["Orbital Speed"] = "V = sqrt((2 * mu)/r - mu/a)"
num_vars["Orbital Speed"] = 4
equations["Orbital Speed"] = orbital_speed
latex_formulas[name] = ""
# 
# 
# 
def escape_speed(solv_vars, vars, dict_val):
    V_escape = vars[0]
    mu = vars[1]
    r = vars[2]

    eq = Eq(V_escape, sqrt((2 * mu)/r))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Escape Speed"
names.append(name)
vars_names["Escape Speed"] = ["Escape Speed", "Standard Gravitational Parameter", "Orbital Radius"]
variables["Escape Speed"] = ["V_escape", "mu", "r"]
formulas["Escape Speed"] = "V_escape = sqrt((2 * mu)/r)"
num_vars["Escape Speed"] = 3
equations["Escape Speed"] = escape_speed
latex_formulas[name] = ""
# 
# 
# 
def orbital_potencial_energy(solv_vars, vars, dict_val):
    U = vars[0]
    mu = vars[1]
    a = vars[2]

    eq = Eq(U, - mu / (2 * a))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Orbital Potencial Energy"
names.append(name)
vars_names["Orbital Potencial Energy"] = ["Orbital Potencial Energy", "Standard Gravitational Parameter", "Semi Major Axis"]
variables["Orbital Potencial Energy"] = ["U", "mu", "a"]
formulas["Orbital Potencial Energy"] = "U = - mu / (2 * a)"
num_vars["Orbital Potencial Energy"] = 3
equations["Orbital Potencial Energy"] = orbital_potencial_energy
latex_formulas[name] = ""
# 
# 
# 
def orbital_period(solv_vars, vars, dict_val):
    T = vars[0]
    a = vars[1]
    mu = vars[2]

    eq = Eq(T, 2 * pi * sqrt(a**3 / mu))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Orbital Period"
names.append(name)
vars_names["Orbital Period"] = ["Orbital Period", "Semi Major Axis", "Standard Gravitational Parameter"]
variables["Orbital Period"] = ["T", "a", "mu"]
formulas["Orbital Period"] = "T = 2 * pi * sqrt(a**3 / mu)"
num_vars["Orbital Period"] = 3
equations["Orbital Period"] = orbital_period
latex_formulas[name] = ""
# 
# 
# 
def standard_gravitational_parameter(solv_vars, vars, dict_val):
    mu = vars[0]
    G = vars[1]
    U = vars[2]

    eq = Eq(mu, G * M)
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Standard Gravitational Parameter"
names.append(name)
vars_names["Standard Gravitational Parameter"] = ["Standard Gravitational Parameter", "Gravitational Constant", "Larger Mass"]
variables["Standard Gravitational Parameter"] = ["mu", "G", "M"]
formulas["Standard Gravitational Parameter"] = "mu = G * M"
num_vars["Standard Gravitational Parameter"] = 3
equations["Standard Gravitational Parameter"] = standard_gravitational_parameter
latex_formulas[name] = ""
# 
# 
# 
def angular_momentum(solv_vars, vars, dict_val):
    H = vars[0]
    mu = vars[1]
    p = vars[2]

    eq = Eq(H, sqrt(mu*p))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Angular Momentum"
names.append(name)
vars_names["Angular Momentum"] = ["Angular Momentum", "Standard Gravitational Parameter", "Focal Para"]
variables["Angular Momentum"] = ["H", "mu", "p"]
formulas["Angular Momentum"] = "H = sqrt(mu*p)"
num_vars["Angular Momentum"] = 3
equations["Angular Momentum"] = angular_momentum
latex_formulas[name] = ""
# 
# 
# 
def radial_speed(solv_vars, vars, dict_val):
    V_r = vars[0]
    mu = vars[1]
    p = vars[2]
    e = vars[3]
    theta = vars[4]

    eq = Eq(V_r, sqrt(mu / p) * e * sin(theta))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Radial Speed"
names.append("Radial Speed")
vars_names["Radial Speed"] = ["Radial Speed", "Standard Gravitational Parameter", "Focal Parameter", "Eccentricity", "Orbital Angle"]
variables["Radial Speed"] = ["V_r", "mu", "p", "e", "theta"]
formulas["Radial Speed"] = "V_r = sqrt(mu / p) * e * sin(theta)"
num_vars["Radial Speed"] = 5
equations["Radial Speed"] = radial_speed
latex_formulas[name] = ""
# 
# 
# 
def normal_speed(solv_vars, vars, dict_val):
    V_n = vars[0]
    mu = vars[1]
    p = vars[2]
    e = vars[3]
    theta = vars[4]

    eq = Eq(V_n, sqrt(mu / p) * (1 + e * cos(theta)))
    result = solve(eq, solv_vars[0], dict=dict_val)

    return result

name = "Normal Speed"
names.append(name)
vars_names[name] = ["Normal Speed", "Standard Gravitational Parameter", "Focal Parameter", "Eccentricity", "Orbital Angle"]
variables[name] = ["V_n", "mu", "p", "e", "theta"]
formulas[name] = "V_n = sqrt(mu / p) * (1 + e * cos(theta))"
num_vars[name] = len(variables[name])
equations[name] = normal_speed
latex_formulas[name] = ""
# 
# 
# 