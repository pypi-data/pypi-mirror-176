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
def Addition(solv_vars, vars, dict_val):
    A = vars[0]
    val_1 = vars[1]
    val_2 = vars[2]

    eq = Eq(A, val_1+val_2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Addition")
vars_names["Addition"] = ["Addition", "Variable 1", "Variable 2"]
variables["Addition"] = ["A", "val_1", "val_2"]
formulas["Addition"] = "A = val_1+val_2"
num_vars["Addition"] = 3
equations["Addition"] = Addition
# 
# 
# 
def Subtraction(solv_vars, vars, dict_val):
    A = vars[0]
    val_1 = vars[1]
    val_2 = vars[2]

    eq = Eq(A, val_1-val_2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Subtraction")
vars_names["Subtraction"] = ["Subtraction", "Variable 1",  "Variable 2"]
variables["Subtraction"] = ["A", "val_1", "val_2"]
formulas["Subtraction"] = "A = val_1-val_2"
num_vars["Subtraction"] = 3
equations["Subtraction"] = Subtraction
# 
# 
# 
def Multiplication(solv_vars, vars, dict_val):
    A = vars[0]
    val_1 = vars[1]
    val_2 = vars[2]

    eq = Eq(A, val_1*val_2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Multiplication")
vars_names["Multiplication"] = ["Multiplication", "Variable 1",  "Variable 2"]
variables["Multiplication"] = ["A", "val_1", "val_2"]
formulas["Multiplication"] = "A = val_1*val_2"
num_vars["Multiplication"] = 3
equations["Multiplication"] = Multiplication
# 
# 
# 
def Division(solv_vars, vars, dict_val):
    A = vars[0]
    val_1 = vars[1]
    val_2 = vars[2]

    eq = Eq(A, val_1/val_2)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Division")
vars_names["Division"] = ["Division", "Variable 1",  "Variable 2"]
variables["Division"] = ["A", "val_1", "val_2"]
formulas["Division"] = "A = val_1/val_2"
num_vars["Division"] = 3
equations["Division"] = Division
# 
# 
# 
def Integer_Division(solv_vars, vars, dict_val):
    A = vars[0]
    val_1 = vars[1]
    val_2 = vars[2]
    R = vars[3]
    
    eq = Eq(A, val_1//val_2 + R)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

names.append("Integer Division")
vars_names["Integer Division"] = ["Division", "Variable 1",  "Variable 2", "Rest"]
variables["Integer Division"] = ["A", "val_1", "val_2", "R"]
formulas["Integer Division"] = "A = val_1/val_2 + R"
num_vars["Integer Division"] = 4
equations["Integer Division"] = Integer_Division
# 
# 
# 