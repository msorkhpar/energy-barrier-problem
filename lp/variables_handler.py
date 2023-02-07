from lp.variables.adjacency_matrix import add_adjacency_matrix_variables
from lp.variables.same_neighborhood_covering import add_neighborhood_variables


def create_variables(solver, g, b, s, l, with_fractional_results):
    number_of_covered_neighborhood = 0
    variables_dictionary = {}

    # adjacency matrix rules
    add_adjacency_matrix_variables(variables_dictionary, g, b, l)
    # neighborhood rules
    number_of_covered_neighborhood += add_neighborhood_variables(variables_dictionary, g, b, s)

    variables = {}
    for index, r in variables_dictionary.items():
        if with_fractional_results:
            variables[index] = solver.NumVar(r[0], r[1], '%i' % index)
        else:
            variables[index] = solver.IntVar(r[0], r[1], '%i' % index)

    # Add k as a variable to the end of list
    if with_fractional_results:
        variables[len(variables_dictionary)] = solver.NumVar(1, len(b), '%i' % (len(variables_dictionary)))
    else:
        variables[len(variables_dictionary)] = solver.IntVar(1, len(b), '%i' % (len(variables_dictionary)))

    return variables, solver.NumVariables(), number_of_covered_neighborhood
