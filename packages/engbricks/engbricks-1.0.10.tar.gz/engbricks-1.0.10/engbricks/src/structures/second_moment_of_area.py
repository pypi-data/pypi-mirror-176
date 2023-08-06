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
def parallel_axis_theorem(solv_vars, vars, dict_val):
    I_new = vars[0]
    I = vars[1]
    A = vars[2]
    d = vars[3]

    eq = Eq(I_new, I + A*d**2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Parallel Axis Theorem'
names.append(name)
vars_names[name] = ['New Second Moment of Area', 'Second Moment of Area', 'Area', 'Axis Distance']
variables[name] = ['I_new', 'I', 'A', 'd']
formulas[name] = 'I_new = I + A*d**2'
num_vars[name] = len(variables[name])
equations[name] = parallel_axis_theorem
# 
# 
# 
def parallel_axis_theorem_product(solv_vars, vars, dict_val):
    I_new = vars[0]
    I = vars[1]
    A = vars[2]
    dx = vars[3]
    dy = vars[4]

    eq = Eq(I_new, I + A*dx*dy)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Parallel Axis Theorem Product of Inertia'
names.append(name)
vars_names[name] = ['New Second Moment of Area', 'Second Moment of Area', 'Area', 'x Axis Distance', 'y Axis Distance']
variables[name] = ['I_new', 'I', 'A', 'dx', 'dy']
formulas[name] = 'I_new = I + A*dx*dy'
num_vars[name] = len(variables[name])
equations[name] = parallel_axis_theorem_product
# 
# 
# 
def second_moment_of_area_xx_rectangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    b = vars[1]
    h = vars[2]

    eq = Eq(Ixx, b*h**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Rectangle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Base', 'Height']
variables[name] = ['Ixx', 'b', 'h']
formulas[name] = 'Ixx = b*h**3/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_rectangle
# 
# 
# 
def second_moment_of_area_yy_rectangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    b = vars[1]
    h = vars[2]

    eq = Eq(Iyy, b**3*h/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Rectangle'
names.append(name)
vars_names[name] = ['Iyy', 'Base', 'Height']
variables[name] = ['Iyy', 'b', 'h']
formulas[name] = 'Iyy = b**3*h/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_rectangle
# 
# 
# 
def second_moment_of_area_xx_hollow_rectangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    b = vars[1]
    h = vars[2]
    bi = vars[3]
    hi = vars[4]

    eq = Eq(Ixx, (b*h**3 - bi*hi**3)/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Hollow Rectangle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Base', 'Height', 'Base Interior', 'Height Interior']
variables[name] = ['Ixx', 'b', 'h', 'bi', 'hi']
formulas[name] = 'Ixx = (b*h**3 - bi*hi**3)/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_hollow_rectangle
# 
# 
# 
def second_moment_of_area_yy_hollow_rectangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    b = vars[1]
    h = vars[2]
    bi = vars[3]
    hi = vars[4]

    eq = Eq(Iyy, (b**3*h - bi**3*hi)/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Hollow Rectangle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Base', 'Height', 'Base Interior', 'Height Interior']
variables[name] = ['Iyy', 'b', 'h', 'bi', 'hi']
formulas[name] = 'Iyy = (b**3*h - bi**3*hi)/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_hollow_rectangle
# 
# 
# 
def second_moment_of_area_xx_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]

    eq = Eq(Ixx, pi * r**4/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Radius']
variables[name] = ['Ixx', 'r']
formulas[name] = 'Ixx = pi * r**4/4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_circle
# 
# 
# 
def second_moment_of_area_yy_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]

    eq = Eq(Iyy, pi * r**4/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Radius']
variables[name] = ['Iyy', 'r']
formulas[name] = 'Iyy = pi * r**4/4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_circle
# 
# 
# 
def second_moment_of_area_xx_hollow_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Ixx, pi * (r**4 - ri**4)/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Hollow Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Radius', 'Radius Interior']
variables[name] = ['Ixx', 'r', 'ri']
formulas[name] = 'Ixx = pi * (r**4 - ri**4)/4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_hollow_circle
# 
# 
# 
def second_moment_of_area_yy_hollow_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Iyy, pi * (r**4 - ri**4)/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Hollow Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Radius', 'Radius Interior']
variables[name] = ['Iyy', 'r', 'ri']
formulas[name] = 'Iyy = pi * (r**4 - ri**4)/4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_hollow_circle
# 
# 
# 
def second_moment_of_area_xx_semi_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]

    eq = Eq(Ixx, (pi/8 - 8/(9*py)) * r**4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Semi-Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Radius']
variables[name] = ['Ixx', 'r']
formulas[name] = 'Ixx = (pi/8 - 8/(9*py)) * r**4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_semi_circle
# 
# 
# 
def second_moment_of_area_yy_semi_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]

    eq = Eq(Iyy, pi * r**4/8)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Semi-Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Radius']
variables[name] = ['Iyy', 'r']
formulas[name] = 'Iyy = pi * r**4/8'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_semi_circle
# 
# 
# 
def second_moment_of_area_xx_hollow_semi_circle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Ixx, pi/8 * (r**4 - ri**4) - pi * 12.1**2 * (r**2 - ri**2)/2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Hollow Semi-Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Radius', 'Radius Interior']
variables[name] = ['Ixx', 'r', 'ri']
formulas[name] = 'Ixx = pi/8 * (r**4 - ri**4) - pi * 12.1**2 * (r**2 - ri**2)/2'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_hollow_semi_circle
# 
# 
# 
def second_moment_of_area_yy_hollow_semi_circle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    r = vars[1]
    ri = vars[2]

    eq = Eq(Iyy, pi/8 * (r**4 - ri**4))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Hollow Semi-Circle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Radius', 'Radius Interior']
variables[name] = ['Iyy', 'r', 'ri']
formulas[name] = 'Iyy = pi/8 * (r**4 - ri**4)'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_hollow_semi_circle
# 
# 
# 
def second_moment_of_area_xx_ellipse(solv_vars, vars, dict_val):
    Ixx = vars[0]
    a = vars[1]
    b = vars[2]

    eq = Eq(Ixx, pi * a/2 * (b/2)**3/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Ellipse'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'x axis size', 'y axis size']
variables[name] = ['Ixx', 'a', 'b']
formulas[name] = 'Ixx = pi * a/2 * (b/2)**3/4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_ellipse
# 
# 
# 
def second_moment_of_area_yy_ellipse(solv_vars, vars, dict_val):
    Iyy = vars[0]
    a = vars[1]
    b = vars[2]

    eq = Eq(Iyy, pi * b/2 * (a/2)**3/4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Ellipse'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'x axis size', 'y axis size']
variables[name] = ['Iyy', 'a', 'b']
formulas[name] = 'Iyy = pi * b/2 * (a/2)**3/4'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_ellipse
# 
# 
# 
def second_moment_of_area_xx_hollow_ellipse(solv_vars, vars, dict_val):
    Ixx = vars[0]
    a = vars[1]
    b = vars[2]
    ai = vars[3]
    bi = vars[4]

    eq = Eq(Ixx, pi/4 * (a/2*(b/2)**3 - ai/2 * (bi/2)**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Hollow Ellipse'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'x axis size', 'y axis size' 'x axis size interior', 'y axis size interior']
variables[name] = ['Ixx', 'a', 'b', 'ai', 'bi']
formulas[name] = 'Ixx = pi/4 * (a/2*(b/2)**3 - ai/2 * (bi/2)**3)'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_hollow_ellipse
# 
# 
# 
def second_moment_of_area_yy_hollow_ellipse(solv_vars, vars, dict_val):
    Iyy = vars[0]
    a = vars[1]
    b = vars[2]
    ai = vars[3]
    bi = vars[4]

    eq = Eq(Iyy, pi/4 * (b/2*(a/2)**3 - bi/2 * (ai/2)**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Hollow Ellipse'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'x axis size', 'y axis size', 'x axis size interior', 'y axis size interior']
variables[name] = ['Ixx', 'a', 'b', 'ai', 'bi']
formulas[name] = 'Iyy = pi * (b/2*(a/2)**3 - bi/2 * (ai/2)**3)'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_hollow_ellipse
# 
# 
# 
def second_moment_of_area_xx_isosceles_triangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    h = vars[1]
    b = vars[2]

    eq = Eq(Ixx, 1/36 * b * h**3)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Isosceles Triangle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Base', 'Height']
variables[name] = ['Ixx', 'h', 'b']
formulas[name] = 'Ixx = 1/36 * b * h**3'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_isosceles_triangle
# 
# 
# 
def second_moment_of_area_yy_isosceles_triangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    h = vars[1]
    b = vars[2]

    eq = Eq(Iyy, 1/48 * b**3 * h)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Isosceles Triangle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Base', 'Height']
variables[name] = ['Iyy', 'h', 'b']
formulas[name] = 'Iyy = 1/48 * b**3 * h'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_isosceles_triangle
# 
# 
# 
def second_moment_of_area_xx_equilateral_triangle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    s = vars[1]

    eq = Eq(Ixx, 0.018 * s**4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Equilateral Triangle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Side']
variables[name] = ['Ixx', 's']
formulas[name] = 'Ixx = 1/36 * b * h**3'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_equilateral_triangle
# 
# 
# 
def second_moment_of_area_yy_equilateral_triangle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    s = vars[1]

    eq = Eq(Iyy, 0.018 * s**4)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Equilateral Triangle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Side']
variables[name] = ['Iyy', 's']
formulas[name] = 'Iyy = 1/36 * b * h**3'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_equilateral_triangle
# 
# 
# 
def second_moment_of_area_xx_tee_section(solv_vars, vars, dict_val):
    Ixx = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Ixx, tw*w**3/3 + (f-tw) * tf**3/3)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Tee Section'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Ixx', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Ixx = tw*w**3/3 + (f-tw) * tf**3/3'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_tee_section
# 
# 
# 
def second_moment_of_area_yy_tee_section(solv_vars, vars, dict_val):
    Iyy = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Iyy, (w-tf) * tw**3/12 + tf*f**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Tee Section'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Iyy', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Iyy = (w-tf) * tw**3/12 + tf*f**3/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_tee_section
# 
# 
# 
def second_moment_of_area_xx_c_channel(solv_vars, vars, dict_val):
    Ixx = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Ixx, f*w**3/12 - (f-tw)*(w-2*tf)**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx C Channel'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Ixx', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Ixx = f*w**3/12 - (f-tw)*(w-2*tf)**3/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_c_channel
# 
# 
# 
def second_moment_of_area_yy_c_channel(solv_vars, vars, dict_val):
    Iyy = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Iyy, f*w**3/12 - (f-tw)*(w-2*tf)**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy C Channel'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Iyy', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Iyy = f*w**3/12 - (f-tw)*(w-2*tf)**3/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_c_channel
# 
# 
# 
def second_moment_of_area_xx_i_section(solv_vars, vars, dict_val):
    Ixx = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Ixx, f*w**3/12 - (f-tw)*(w-2*tf)**3/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx I Section'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Ixx', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Ixx = f*w**3/12 - (f-tw)*(w-2*tf)**3/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_i_section
# 
# 
# 
def second_moment_of_area_yy_i_section(solv_vars, vars, dict_val):
    Iyy = vars[0]
    f = vars[1]
    w = vars[2]
    tf = vars[3]
    tw = vars[4]

    eq = Eq(Iyy, (w-2*tf)*tw**3/12 + 2*(tf*f**3)/12)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy I Section'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Flange', 'web', 'Flange Thickness', 'Web Thickness']
variables[name] = ['Iyy', 'f', 'w', 'tf', 'tw']
formulas[name] = 'Iyy = (w-2*tf)*tw**3/12 + 2*(tf*f**3)/12'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_i_section
# 
# 
# 
def second_moment_of_area_xx_angle(solv_vars, vars, dict_val):
    Ixx = vars[0]
    h = vars[1]
    b = vars[2]
    t = vars[3]

    eq = Eq(Ixx, t/3 * (b*t**2 + h**3 - t**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Ixx Angle'
names.append(name)
vars_names[name] = ['Second Moment of Area x', 'Height', 'Base', 'Thickness']
variables[name] = ['Ixx', 'h', 'b', 't']
formulas[name] = 'Ixx = t/3 * (b*t**2 + h**3 - t**3)'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_xx_angle
# 
# 
# 
def second_moment_of_area_yy_angle(solv_vars, vars, dict_val):
    Iyy = vars[0]
    h = vars[1]
    b = vars[2]
    t = vars[3]

    eq = Eq(Iyy, t/3 * (h*t**2 + b**3 - t**3))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Second Moment of Area Iyy Angle'
names.append(name)
vars_names[name] = ['Second Moment of Area y', 'Height', 'Base', 'Thickness']
variables[name] = ['Iyy', 'h', 'b', 't']
formulas[name] = 'Iyy = t/3 * (h*t**2 + b**3 - t**3)'
num_vars[name] = len(variables[name])
equations[name] = second_moment_of_area_yy_angle
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