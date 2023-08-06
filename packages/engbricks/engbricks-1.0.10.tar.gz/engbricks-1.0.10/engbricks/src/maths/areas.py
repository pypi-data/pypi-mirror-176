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
#2D shapes
def Rectangle_Area(solv_vars, vars, dict_val):
    A = vars[0]
    side_a = vars[1]
    side_b = vars[2]

    eq = Eq(A, side_a*side_b)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Rectangle Area")
vars_names["Rectangle Area"] = ["Area", "Side A", "Side B"]
variables["Rectangle Area"] = ["A", "side_a", "side_b"]
formulas["Rectangle Area"] = "A = side_a*side_b"
num_vars["Rectangle Area"] = 3
equations["Rectangle Area"] = Rectangle_Area
# 
# 
# 
def Circle_Area(solv_vars, vars, dict_val):
    A = vars[0]
    r = vars[1]

    eq = Eq(A, pi * r**2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Circle")
vars_names["Circle"] = ["Area", "Radius"]
variables["Circle"] = ["A", "r"]
formulas["Circle"] = "A = pi * r^2"
num_vars["Circle"] = 2
equations["Circle"] = Circle_Area
# 
# 
# 
def Ellipse(solv_vars, vars, dict_val):
    A = vars[0]
    a = vars[1]
    b = vars[2]

    eq = Eq(A, pi * a * b)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Ellipse")
vars_names["Ellipse"] = ["Area", "Semi-major", "Semi-minor"]
variables["Ellipse"] = ["A", "a", "b"]
formulas["Ellipse"] = "A = pi * a * b"
num_vars["Ellipse"] = 3
equations["Ellipse"] = Ellipse
# 
# 
# 
def Trapezoid(solv_vars, vars, dict_val):
    A = vars[0]
    a = vars[1]
    b = vars[2]
    h = vars[3]

    eq = Eq(A, (a + b)/2 * h)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Trapezoid")
vars_names["Trapezoid"] = ["Area", "Base a", "Base b", "Height"]
variables["Trapezoid"] = ["A", "a", "b", "h"]
formulas["Trapezoid"] = "A = (a + b)/2 * h"
num_vars["Trapezoid"] = 4
equations["Trapezoid"] = Ellipse
# 
# 
# 
def Triangle(solv_vars, vars, dict_val):
    A = vars[0]
    a = vars[1]
    h = vars[2]

    eq = Eq(A, a * h/2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Triangle")
vars_names["Triangle"] = ["Area", "Base", "Height"]
variables["Triangle"] = ["A", "a", "h"]
formulas["Triangle"] = "A = a * h/2"
num_vars["Triangle"] = 3
equations["Triangle"] = Triangle
# 
# 
# 
def Parallelogram(solv_vars, vars, dict_val):
    A = vars[0]
    b = vars[1]
    h = vars[2]

    eq = Eq(A, b * h)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Parallelogram")
vars_names["Parallelogram"] = ["Area", "Base", "Height"]
variables["Parallelogram"] = ["A", "b", "h"]
formulas["Parallelogram"] = "A = b * h"
num_vars["Parallelogram"] = 3
equations["Parallelogram"] = Parallelogram
# 
# 
# 
def Regular_Hexagon(solv_vars, vars, dict_val):
    A = vars[0]
    s = vars[1]

    eq = Eq(A, 3/2 * sqrt(3) * s**2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Regular Hexagon")
vars_names["Regular Hexagon"] = ["Area", "Side"]
variables["Regular Hexagon"] = ["A", "s"]
formulas["Regular Hexagon"] = "A = 3/2 * sqrt(3) * s**2"
num_vars["Regular Hexagon"] = 2
equations["Regular Hexagon"] = Regular_Hexagon
# 
# 
# 
def Regular_Octagon(solv_vars, vars, dict_val):
    A = vars[0]
    s = vars[1]

    eq = Eq(A, 2 * (1 + sqrt(2)) * s**2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Regular Octagon")
vars_names["Regular Octagon"] = ["Area", "Side"]
variables["Regular Octagon"] = ["A", "s"]
formulas["Regular Octagon"] = "A = 2 * (1 + sqrt(2)) * s**2"
num_vars["Regular Octagon"] = 2
equations["Regular Octagon"] = Regular_Octagon
# 
# 
# 
#3D solids
def Sphere_surface(solv_vars, vars, dict_val):
    A = vars[0]
    r = vars[1]

    eq = Eq(A, 4 * pi * r**2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Sphere Surface")
vars_names["Sphere Surface"] = ["Area", "Radius"]
variables["Sphere Surface"] = ["A", "r"]
formulas["Sphere Surface"] = "A = 4 * pi * r**2"
num_vars["Sphere Surface"] = 3
equations["Sphere Surface"] = Sphere_surface
# 
# 
# 
def Cylinder_total_surface(solv_vars, vars, dict_val):
    A = vars[0]
    r = vars[1]
    h = vars[3]

    eq = Eq(A, 4 * pi * r * (r + h))

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Cylinder Total Surface")
vars_names["Cylinder Total Surface"] = ["Area", "Radius", "Height"]
variables["Cylinder Total Surface"] = ["A", "r", "h"]
formulas["Cylinder Total Surface"] = "A = 4 * pi * r * (r + h)"
num_vars["Cylinder Total Surface"] = 3
equations["Cylinder Total Surface"] = Cylinder_total_surface
# 
# 
# 