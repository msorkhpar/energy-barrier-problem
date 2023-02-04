from lp.variables.adjacency_matrix import add_adjacency_matrix_variables
from lp.variables.degree_ones import add_degree_ones_variables
from lp.variables.same_neighborhood_covering import add_neighborhood_variables


def create_variables(solver, g, b, s, l, with_fractional_results):
    number_of_covered_neighborhood = 0
    vars_dict = {}

    # adjacency matrix rules
    add_adjacency_matrix_variables(vars_dict, g, b, l)
    # neighborhood rules
    number_of_covered_neighborhood += add_neighborhood_variables(vars_dict, g, b,s)
    # degree one rules
    add_degree_ones_variables(vars_dict, g, b, l)

    variables = {}
    for index, r in vars_dict.items():
        if with_fractional_results:
            variables[index] = solver.NumVar(r[0], r[1], '%i' % index)
        else:
            variables[index] = solver.IntVar(r[0], r[1], '%i' % index)

    # Add k as a variable to the end of list
    if with_fractional_results:
        variables[len(vars_dict)] = solver.NumVar(1, len(b), '%i' % (len(vars_dict)))
    else:
        variables[len(vars_dict)] = solver.IntVar(1, len(b), '%i' % (len(vars_dict)))

    return variables, solver.NumVariables(), number_of_covered_neighborhood
