from sympy import latex, solve, pprint, Eq, symbols
from sympy import pi, sqrt, ln, sin, cos, tan, atan, exp, Pow
import json
# 
# 
# 
mods = {
    "Arithmetic":                  "src.maths.arithmetic",
    "Area":                        "src.maths.areas",
    "Probability":                 "src.maths.probability",
    "Trigonometry":                "src.maths.trigonometry",
    "Aircraft":                    "src.aircraft_performance.performance_aircraft",
    "Wing":                        "src.aircraft_performance.performance_wing",
    "Propulsion":                  "src.aircraft_performance.performance_propulsion",
    "Take-Off":                    "src.aircraft_performance.performance_takeoff",
    "Climb":                       "src.aircraft_performance.performance_climb",
    "Cruise":                      "src.aircraft_performance.performance_cruise",
    "Cruise Jet":                  "src.aircraft_performance.performance_jet_cruise",
    "Cruise Propeller":            "src.aircraft_performance.performance_propeller_cruise",
    "Landing":                     "src.aircraft_performance.performance_landing",
    "Glide":                       "src.aircraft_performance.performance_glide",
    "Turn":                        "src.aircraft_performance.performance_turn",
    "Looping":                     "src.aircraft_performance.performance_looping",
    "Structures Vibration":        "src.structures.vibration",
    "Second Moment of Area":       "src.structures.second_moment_of_area",
    "Composites":                  "src.structures.composites",
    "Astrodynamics":               "src.astrodynamics",
    "Jet Propulsion":              "src.jet_propulsion",
    "Atmosphere":                  "src.atmosphere",
    "User":                        "src.user_equations"
}
# 
# 
# 
def list_modules():
    for mod in mods:
        print("[+]", mod)
# 
# 
# 
def list_formulas(module_name:str):
    try:
        module_path = mods[module_name]
        module = __import__(module_path, fromlist=[None])

        for formula in module.names:
            print("[+]", formula)

    except Exception as ex:
        print("[+] Error:", ex)
# 
# 
# 
def list_all():
    for mod_key, mod_value in mods.items():
        module = __import__(mod_value, fromlist=[None])

        print("[+]", mod_key)

        for formula in module.names:
            print("\t[+]", formula)

        print()
# 
# 
# 
def view_formula(module_name:str, formula_name:str, pretty_print:bool=False):
    local_namespace = {"Eq":Eq, "symbols":symbols, "pi":pi, "sqrt":sqrt, "ln":ln, "sin":sin, "cos":cos, "tan":tan, "atan":atan, "exp":exp, "Pow":Pow}

    try:
        module_path = mods[module_name]
        module = __import__(module_path, fromlist=[None])

        formula = module.formulas[formula_name]
        variables = module.variables[formula_name]
        
        if pretty_print:
            for variable in variables:
                variable_name = variable
                aux = "{}=symbols('{}')".format(variable, variable)
                exec(aux, local_namespace)

            exec("expr = Eq(" + formula.split("=")[0].replace("^", "**") + "," + formula.split("=")[1].replace("^", "**") + ")", local_namespace)

            pprint(local_namespace["expr"], use_unicode=True)

        else:
            print(formula)

        print()

    except Exception as ex:
        print("[+] Error:", ex)
# 
# 
# 
def view_formula_latex(module_name:str, formula_name:str):
    local_namespace = {"Eq":Eq, "symbols":symbols, "pi":pi, "sqrt":sqrt, "ln":ln, "sin":sin, "cos":cos, "tan":tan, "atan":atan, "exp":exp, "Pow":Pow}

    try:
        module_path = mods[module_name]
        module = __import__(module_path, fromlist=[None])

        formula = module.formulas[formula_name]
        variables = module.variables[formula_name]
        
        for variable in variables:
            variable_name = variable
            aux = "{}=symbols('{}')".format(variable, variable)
            exec(aux, local_namespace)

        exec("expr = Eq(" + formula.split("=")[0].replace("^", "**") + "," + formula.split("=")[1].replace("^", "**") + ")", local_namespace)

        # pprint(local_namespace["expr"], use_unicode=True)

        formula_latex = latex(local_namespace["expr"])
        print(formula_latex)

        print()

    except Exception as ex:
        print("[+] Error:", ex)
# 
# 
# 
class formulas_queue():
    def __init__(self, name):
        self.name = name
        # formulas is 
        self.formulas = list()
        self.variables = dict()
        self.variables_multi = dict()
        self.namespace = {"Eq":Eq, "symbols":symbols, "pi":pi, "sqrt":sqrt, "ln":ln, "sin":sin, "cos":cos, "tan":tan, "atan":atan, "exp":exp, "Pow":Pow}
    # 
    # 
    def add_formula(self, module_name:str, formula_name:str, solve_to:str=None):
        local_namespace = self.namespace.copy()

        try:
            # import module
            module_path = mods[module_name]
            module = __import__(module_path, fromlist=[None])

            # get formula and variables
            formula = module.formulas[formula_name]
            formula_variables = module.variables[formula_name]

            for variable in formula_variables:
                self.variables[variable] = variable

            # if solve_to variableis not passed use the formula default
            if not solve_to:
                solve_to = formula.split("=")[0].strip()

            self.formulas.append([module_name, formula_name, formula, formula_variables, solve_to])

        except Exception as ex:
            print("[+] Error:", ex)
    # 
    # 
    def print_formulas(self, default:bool=True):
        local_namespace = self.namespace.copy()
        print("-"*50)

        # print default
        if default:
            i = 0
            for formula in self.formulas:
                print(i, "-", formula[0], "-", formula[1])

                # create variables to create symbols
                for variable in formula[3]:
                    aux = "{}=symbols('{}')".format(variable, variable)
                    exec(aux, local_namespace)
                
                # create formula eq
                aux = "expr = Eq({},{})".format(formula[2].split("=")[0].replace("^", "**"), formula[2].split("=")[1].replace("^", "**"))
                exec(aux, local_namespace)

                # print formula
                pprint(local_namespace["expr"], use_unicode=True)
                print("-"*50)
                i += 1

        # print in order to solve_to
        else:
            i = 0
            for formula in self.formulas:
                print(i, "-", formula[0], "-", formula[1])

                # create variables to create symbols
                for variable in formula[3]:
                    aux = "{}=symbols('{}')".format(variable, variable)
                    exec(aux, local_namespace)
                
                # create symbol for solving variable
                aux = "{}=symbols('{}')".format(formula[4], formula[4])
                exec(aux, local_namespace)

                # create formula eq
                aux = "expr = Eq({},{})".format(formula[2].split("=")[0].replace("^", "**"), formula[2].split("=")[1].replace("^", "**"))
                exec(aux, local_namespace)

                # solve Eq
                results = solve(local_namespace["expr"], local_namespace[formula[4]])

                aux = "expr = Eq({},{})".format(formula[4], results[0])
                exec(aux, local_namespace)

                # print formula
                pprint(local_namespace["expr"], use_unicode=True)
                print("-"*50)
                i += 1

    # 
    # 
    def reorder_formula(self, formula_id, new_formula_id):
        try:
            aux = self.formulas[formula_id]
            self.formulas.remove(aux)
            self.formulas.insert(new_formula_id, aux)

        except Exception as ex:
            print("[+] Error:", ex)
    # 
    # 
    def change_formula_solve_to(self, formula_id, new_solve_to):
        try:
            self.formulas[formula_id][4] = new_solve_to

        except Exception as ex:
            print("[+] Error:", ex)
    # 
    # 
    def print_variables(self):
        for variable_key, variable_value in self.variables.items():
            print("{0:<5} ---> {1}".format(variable_key, str(variable_value)))

        print()
    # 
    # 
    def set_variable(self, variables_name, variable_value):
        self.variables[variables_name] = variable_value
    # 
    # 
    def change_variable(self, variables_name, variables_new_name):
        self.variables[variables_name] = variable_value
    # 
    # 
    def reset_variable(self):
        for variable in self.variables:
            self.variables[variable] = variable
    # 
    # 
    def calculate(self):
        local_namespace = self.namespace.copy()

        # iterate over formulas
        for formula in self.formulas:

            # iterate over variables to create symbols
            # need to do it like this because variables that depend on other variables
            variables = formula[3].copy()
            for variable in variables:
                # if variable has an error skip it
                try:
                    aux = "{}=symbols('{}')".format(variable, variable)
                    exec(aux, local_namespace)

                    aux = "{}={}".format(variable, self.variables[variable])
                    exec(aux, local_namespace)

                # and add it to the end of the queue
                except:
                    variables.append(variable)

            # create symbols for solving variable
            aux = "{}=symbols('{}')".format(formula[4], formula[4])
            exec(aux, local_namespace)

            # create formula Eq
            aux = "expr = Eq({},{})".format(formula[2].split("=")[0].replace("^", "**"), formula[2].split("=")[1].replace("^", "**"))
            exec(aux, local_namespace)

            # solve Eq
            results = solve(local_namespace["expr"], local_namespace[formula[4]], dict=True)
            # print(results)

            # update variables dict
            for result_key, result_value in results[0].items():
                self.variables[str(result_key)] = result_value

            print(formula[4], "=", self.variables[formula[4]])
        
        print()
        self.print_variables()
    # 
    # 
    def calculate_multi(self):
        pass
# 
# 
# 
if __name__ == "__main__":
    # list()
    # list_modules()
    # list_formulas("Area")
    # list_all()
    view_formula("Aircraft", "H.T. Volume Coef", True)
    view_formula_latex("Aircraft", "H.T. Volume Coef")

    # q1 = formulas_queue("q3ew1")
    # print(q1.name)

    # q1.add_formula("Aircraft", "H.T. Volume Coef", "mac")

    # q1.print_formulas()
    # q1.print_variables()

    # q1.set_variable("S_w", 154)
    # q1.set_variable("L_h", 10.3)
    # q1.set_variable("V_h", 21)
    # q1.set_variable("S_h", 100)

    # q1.print_variables()

    # q1.set_variable("A", 100)
    # q1.set_variable("r", 100)

    # q1.add_formula("Area", "Circle", "A")
    # q1.print_formulas()

    # q1.set_variable("r", 10)

    # q1.calculate()
    # q1.print_formulas()
    # q1.print_variables()


    # q1.set_variable("mac", 100)
    # q1.set_variable("A", "mac")
    # q1.calculate()
    # q1.print_variables()


    # q1.reorder_formula(3, 0)
    # q1.print_formulas()

    # q1.set_variable("S_h", "mac")
    # q1.change_formula_solve_to(0, "S_w")
    # q1.calculate()
#   
# 
# 