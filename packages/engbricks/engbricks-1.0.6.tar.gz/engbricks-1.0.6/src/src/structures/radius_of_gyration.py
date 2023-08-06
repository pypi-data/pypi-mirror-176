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
def radius_of_gyration_x_rectangle(solv_vars, vars, dict_val):
    Rg_x = vars[0]
    Ixx = vars[1]
    A = vars[2]

    eq = Eq(Rg_x, sqrt(Ixx/A))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Rgx rectangle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Radius of Gyration x', 'Area']
variables[name] = ['Rgx', 'Ixx', 'A']
formulas[name] = 'Rgx = sqrt(Ixx/A)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_x_rectangle
# 
# 
# 
def radius_of_gyration_y_rectangle(solv_vars, vars, dict_val):
    Rg_y = vars[0]
    Iyy = vars[1]
    A = vars[2]

    eq = Eq(Rg_y, sqrt(Iyy/A))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Rgy rectangle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Radius of Gyration y', 'Area']
variables[name] = ['Rgy', 'Iyy', 'A']
formulas[name] = 'Rgy = sqrt(Iyy/A)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_y_rectangle
# 
# 
# 
def radius_of_gyration_xx_hollow_rectangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    b = vars[1]
    h = vars[2]
    bi = vars[3]
    hi = vars[4]

    eq = Eq(Ixx, (b*h**3 - bi*hi**3)/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Hollow Rectangle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Base', 'Height', 'Base Interior', 'Height Interior']
variables[name] = ['Ixx', 'b', 'h', 'bi', 'hi']
formulas[name] = 'Ixx = (b*h**3 - bi*hi**3)/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_hollow_rectangle
# 
# 
# 
def radius_of_gyration_yy_hollow_rectangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    b = vars[1]
    h = vars[2]
    bi = vars[3]
    hi = vars[4]

    eq = Eq(Iyy, (b**3*h - bi**3*hi)/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Hollow Rectangle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Base', 'Height', 'Base Interior', 'Height Interior']
variables[name] = ['Iyy', 'b', 'h', 'bi', 'hi']
formulas[name] = 'Iyy = (b**3*h - bi**3*hi)/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_hollow_rectangle
# 
# 
# 
def radius_of_gyration_xx_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]

    eq = Eq(Ixx, pi * r**4/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Radius']
variables[name] = ['Ixx', 'r']
formulas[name] = 'Ixx = pi * r**4/4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_circle
# 
# 
# 
def radius_of_gyration_yy_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]

    eq = Eq(Iyy, pi * r**4/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Radius']
variables[name] = ['Iyy', 'r']
formulas[name] = 'Iyy = pi * r**4/4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_circle
# 
# 
# 
def radius_of_gyration_xx_hollow_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Ixx, pi * (r**4 - ri**4)/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Hollow Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Radius', 'Radius Interior']
variables[name] = ['Ixx', 'r', 'ri']
formulas[name] = 'Ixx = pi * (r**4 - ri**4)/4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_hollow_circle
# 
# 
# 
def radius_of_gyration_yy_hollow_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Iyy, pi * (r**4 - ri**4)/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Hollow Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Radius', 'Radius Interior']
variables[name] = ['Iyy', 'r', 'ri']
formulas[name] = 'Iyy = pi * (r**4 - ri**4)/4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_hollow_circle
# 
# 
# 
def radius_of_gyration_xx_semi_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]

    eq = Eq(Ixx, (pi/8 - 8/(9*py)) * r**4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Semi-Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Radius']
variables[name] = ['Ixx', 'r']
formulas[name] = 'Ixx = (pi/8 - 8/(9*py)) * r**4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_semi_circle
# 
# 
# 
def radius_of_gyration_yy_semi_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]

    eq = Eq(Iyy, pi * r**4/8)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Semi-Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Radius']
variables[name] = ['Iyy', 'r']
formulas[name] = 'Iyy = pi * r**4/8'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_semi_circle
# 
# 
# 
def radius_of_gyration_xx_hollow_semi_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Ixx, pi/8 * (r**4 - ri**4) - pi * 12.1**2 * (r**2 - ri**2)/2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Hollow Semi-Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Radius', 'Radius Interior']
variables[name] = ['Ixx', 'r', 'ri']
formulas[name] = 'Ixx = pi/8 * (r**4 - ri**4) - pi * 12.1**2 * (r**2 - ri**2)/2'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_hollow_semi_circle
# 
# 
# 
def radius_of_gyration_yy_hollow_semi_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Iyy, pi/8 * (r**4 - ri**4))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Hollow Semi-Circle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Radius', 'Radius Interior']
variables[name] = ['Iyy', 'r', 'ri']
formulas[name] = 'Iyy = pi/8 * (r**4 - ri**4)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_hollow_semi_circle
# 
# 
# 
def radius_of_gyration_xx_ellipse(solv_vars, vars, dict_val):
    Ixx = vars[0]
    a = vars[1]
    b = vars[2]

    eq = Eq(Ixx, pi * a/2 * (b/2)**3/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Ellipse'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'x axis size', 'y axis size']
variables[name] = ['Ixx', 'a', 'b']
formulas[name] = 'Ixx = pi * a/2 * (b/2)**3/4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_ellipse
# 
# 
# 
def radius_of_gyration_yy_ellipse(solv_vars, vars, dict_val):
    Iyy = vars[0]
    a = vars[1]
    b = vars[2]

    eq = Eq(Iyy, pi * b/2 * (a/2)**3/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Ellipse'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'x axis size', 'y axis size']
variables[name] = ['Iyy', 'a', 'b']
formulas[name] = 'Iyy = pi * b/2 * (a/2)**3/4'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_ellipse
# 
# 
# 
def radius_of_gyration_xx_hollow_ellipse(solv_vars, vars, dict_val):
    Ixx = vars[0]
    a = vars[1]
    b = vars[2]
    ai = vars[3]
    bi = vars[4]

    eq = Eq(Ixx, pi/4 * (a/2*(b/2)**3 - ai/2 * (bi/2)**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Hollow Ellipse'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'x axis size', 'y axis size' 'x axis size interior', 'y axis size interior']
variables[name] = ['Ixx', 'a', 'b', 'ai', 'bi']
formulas[name] = 'Ixx = pi/4 * (a/2*(b/2)**3 - ai/2 * (bi/2)**3)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_hollow_ellipse
# 
# 
# 
def radius_of_gyration_yy_hollow_ellipse(solv_vars, vars, dict_val):
    Iyy = vars[0]
    a = vars[1]
    b = vars[2]
    ai = vars[3]
    bi = vars[4]

    eq = Eq(Iyy, pi/4 * (b/2*(a/2)**3 - bi/2 * (ai/2)**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Hollow Ellipse'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'x axis size', 'y axis size', 'x axis size interior', 'y axis size interior']
variables[name] = ['Ixx', 'a', 'b', 'ai', 'bi']
formulas[name] = 'Iyy = pi * (b/2*(a/2)**3 - bi/2 * (ai/2)**3)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_hollow_ellipse
# 
# 
# 
def radius_of_gyration_xx_isosceles_triangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    h = vars[1]
    b = vars[2]

    eq = Eq(Ixx, 1/36 * b * h**3)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Isosceles Triangle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Base', 'Height']
variables[name] = ['Ixx', 'h', 'b']
formulas[name] = 'Ixx = 1/36 * b * h**3'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_isosceles_triangle
# 
# 
# 
def radius_of_gyration_yy_isosceles_triangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    h = vars[1]
    b = vars[2]

    eq = Eq(Iyy, 1/48 * b**3 * h)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Isosceles Triangle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Base', 'Height']
variables[name] = ['Iyy', 'h', 'b']
formulas[name] = 'Iyy = 1/48 * b**3 * h'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_isosceles_triangle
# 
# 
# 
def radius_of_gyration_xx_equilateral_triangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    s = vars[1]

    eq = Eq(Ixx, 0.018 * s**4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Equilateral Triangle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Side']
variables[name] = ['Ixx', 's']
formulas[name] = 'Ixx = 1/36 * b * h**3'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_equilateral_triangle
# 
# 
# 
def radius_of_gyration_yy_equilateral_triangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    s = vars[1]

    eq = Eq(Iyy, 0.018 * s**4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Equilateral Triangle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Side']
variables[name] = ['Iyy', 's']
formulas[name] = 'Iyy = 1/36 * b * h**3'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_equilateral_triangle
# 
# 
# 
def radius_of_gyration_xx_tee_section(solv_vars, vars, dict_val):
    Ixx = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Ixx, tw*w**3/3 + (f-tw) * tf**3/3)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Tee Section'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Ixx', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Ixx = tw*w**3/3 + (f-tw) * tf**3/3'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_tee_section
# 
# 
# 
def radius_of_gyration_yy_tee_section(solv_vars, vars, dict_val):
    Iyy = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Iyy, (w-tf) * tw**3/12 + tf*f**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Tee Section'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Iyy', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Iyy = (w-tf) * tw**3/12 + tf*f**3/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_tee_section
# 
# 
# 
def radius_of_gyration_xx_c_channel(solv_vars, vars, dict_val):
    Ixx = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Ixx, f*w**3/12 - (f-tw)*(w-2*tf)**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx C Channel'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Ixx', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Ixx = f*w**3/12 - (f-tw)*(w-2*tf)**3/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_c_channel
# 
# 
# 
def radius_of_gyration_yy_c_channel(solv_vars, vars, dict_val):
    Iyy = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Iyy, f*w**3/12 - (f-tw)*(w-2*tf)**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy C Channel'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Iyy', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Iyy = f*w**3/12 - (f-tw)*(w-2*tf)**3/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_c_channel
# 
# 
# 
def radius_of_gyration_xx_i_section(solv_vars, vars, dict_val):
    Ixx = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Ixx, f*w**3/12 - (f-tw)*(w-2*tf)**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx I Section'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Ixx', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Ixx = f*w**3/12 - (f-tw)*(w-2*tf)**3/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_i_section
# 
# 
# 
def radius_of_gyration_yy_i_section(solv_vars, vars, dict_val):
    Iyy = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Iyy, (w-2*tf)*tw**3/12 + 2*(tf*f**3)/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy I Section'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Iyy', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Iyy = (w-2*tf)*tw**3/12 + 2*(tf*f**3)/12'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_i_section
# 
# 
# 
def radius_of_gyration_xx_angle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    h = vars[1]
    b = vars[2]
    t = vars[3]

    eq = Eq(Ixx, t/3 * (b*t**2 + h**3 - t**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Ixx Angle'
names.append(name)
vars_names[name] = ['Radius of Gyration x', 'Height', 'Base', 'Thickness']
variables[name] = ['Ixx', 'h', 'b', 't']
formulas[name] = 'Ixx = t/3 * (b*t**2 + h**3 - t**3)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_xx_angle
# 
# 
# 
def radius_of_gyration_yy_angle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    h = vars[1]
    b = vars[2]
    t = vars[3]

    eq = Eq(Iyy, t/3 * (h*t**2 + b**3 - t**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Radius of Gyration Iyy Angle'
names.append(name)
vars_names[name] = ['Radius of Gyration y', 'Height', 'Base', 'Thickness']
variables[name] = ['Iyy', 'h', 'b', 't']
formulas[name] = 'Iyy = t/3 * (h*t**2 + b**3 - t**3)'
num_vars[name] = len(variables[name])
equations[name] = radius_of_gyration_yy_angle
# 
# 
# 




# def aaa(solv_vars, vars, dict_val):
#     aaa = vars[0]
#     aaa = vars[1]
#     aaa = vars[2]

#     eq = Eq(aaa, aaa/aaa)

#     results = solve(eq, solv_vars[0], dict = dict_val)

#     return results

# name = 'aaa'
# names.append(name)
# vars_names[name] = ['aaa', 'aaa', 'aaa']
# variables[name] = ['aaa', 'aaa', 'aaa']
# formulas[name] = 'aaa = aaa/aaa'
# num_vars[name] = len(variables[name])
# equations[name] = aaa
# 
# 
# 