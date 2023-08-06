# Engineering Bricks
## Instalation
pip install engbricks

## Classes
formulas_queue

## Formulas
list_all

list_modules

list_formulas

view_formula

view_formula_latex

## Usage

### Lista available modules
engbricks.list_modules()


### Lista available module functions
engbricks.list_formulas("Arithmetic")

### View a formula
engbricks.view_formula("Arithmetic", "Subtraction", True)

or to get in latex

engbricks.view_formula_latex("Arithmetic", "Subtraction")

## Create a new queue to calculate
q = engbricks.formulas_queue("Queue 1")

q.add_formula("Arithmetic", "Subtraction")

q.add_formula("Arithmetic", "Addition")

q.print_formulas()

q.print_variables()

