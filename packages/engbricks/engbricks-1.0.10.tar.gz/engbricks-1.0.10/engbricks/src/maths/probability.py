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
def conditional_probability(solv_vars, vars, dict_val):
    P_A_B = vars[0]
    P_A_and_B = vars[1]
    P_B = vars[2]

    eq = Eq(P_A_B, P_A_and_B/P_B)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Conditional Probability'
names.append(name)
vars_names[name] = ['P(A|B)', 'P(A and B)', 'P(B)']
variables[name] = ['P_A_B', 'P_A_and_B', 'P_B']
formulas[name] = 'P(A|B) = P(A and B)/P(B)'
num_vars[name] = 3
equations[name] = conditional_probability
# 
# 
# 
def independent_events(solv_vars, vars, dict_val):
    P_A_and_B = vars[0]
    P_A = vars[1]
    P_B = vars[2]

    eq = Eq(P_A_and_B, P_A * P_B)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Independent Events'
names.append(name)
vars_names[name] = ['P(A and B)', 'P(A)', 'P(B)']
variables[name] = ['P_A_and_B', 'P_A', 'P_B']
formulas[name] = 'P(A and B) = P(A) * P(B)'
num_vars[name] = 3
equations[name] = independent_events
# 
# 
# 
def mutually_exclusive_events(solv_vars, vars, dict_val):
    P_A_or_B = vars[0]
    P_A = vars[1]
    P_B = vars[2]

    eq = Eq(P_A_or_B, P_A + P_B)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Mutually Exclusive Events'
names.append(name)
vars_names[name] = ['P(A or B)', 'P(A)', 'P(B)']
variables[name] = ['P_A_or_B', 'P_A', 'P_B']
formulas[name] = 'P(A or B) = P(A) + P(B)'
num_vars[name] = 3
equations[name] = mutually_exclusive_events
# 
# 
# 
def not_mutually_exclusive_events(solv_vars, vars, dict_val):
    P_A_or_B = vars[0]
    P_A = vars[1]
    P_B = vars[2]
    P_A_and_B = vars[3]

    eq = Eq(P_A_or_B, P_A + P_B - P_A_and_B)

    results = solve(eq, solv_vars[0], dict = dict_val)

    return results

name = 'Not Mutually Exclusive Events'
names.append(name)
vars_names[name] = ['P(A or B)', 'P(A)', 'P(B)', 'P(A and B)']
variables[name] = ['P_A_or_B', 'P_A', 'P_B', "P_A_and_B"]
formulas[name] = 'P(A or B) = P(A) + P(B) - P(A and B)'
num_vars[name] = 4
equations[name] = not_mutually_exclusive_events
# 
# 
# 