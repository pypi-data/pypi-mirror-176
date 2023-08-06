import urllib.request

from sympy import symbols, preview, Symbol
import sympy as sym

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


import astrodynamics


# start selenium driver
driver = webdriver.Chrome()

driver.get("http://www.latex2png.com/")

assert "latex2png" in driver.title

wait = WebDriverWait(driver, 10)


# find equation field
elem = driver.find_element_by_id("form_latex")

# loop through equations

for variables_list, formula, formula_name in zip(astrodynamics.variables.values(), astrodynamics.formulas.values(), astrodynamics.names):
	# print(variables_list)
	# print(formula)
	# print(formula_name)
	# print("\n\n")

	elem.clear()


	# create symbols
	variables = ''.join(str(e + ",") for e in variables_list)
	variables = variables[:-1]

	variables_code = variables + " = sym.symbols('" + variables + "')"

	exec(variables_code)


	# create expression
	if "sin" in formula:
		formula = formula.replace("sin", "sym.sin")
	
	if "cos" in formula:
		formula = formula.replace("cos", "sym.cos")
	
	if "tan" in formula:
		formula = formula.replace("tan", "sym.tan")

	if "sqrt" in formula:
		formula = formula.replace("sqrt", "sym.sqrt")

	if "pi" in formula:
		formula = formula.replace("pi", "sym.pi")

	form1, form2 = formula.split("=")

	formula_code = "expr = sym.Eq(" + form1 + "," + form2 + ")"

	exec(formula_code)


	# create latex formula
	equation_code = "equation_code = sym.Eq(" + form1 + "," + form2 + ")"
	exec(equation_code)

	equation_latex = sym.latex(equation_code)
	# print(equation_latex)

	# save to png
	# filename = 'output.png'
	# preview(expr, output='png', viewer='file', euler=True, packages=(), filename=filename, outputbuffer=None, preamble=None, dvioptions=None, outputTexFile=None)

	elem.send_keys(equation_latex)

	file_name = formula_name + ".png"


	# click in the button
	# elem.send_keys(Keys.RETURN)
	driver.find_element_by_id("convert_button").click()

	time.sleep(2)


	# download the image
	img = driver.find_element_by_id("img_output")

	src = img.get_attribute('src')

	urllib.request.urlretrieve(src, file_name)


# finalize and close driver
assert "No results found." not in driver.page_source

driver.close()