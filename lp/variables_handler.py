import sys

from lp.solver import Parameters
from lp.variables.adjacency_matrix import add_adjacency_matrix_variables
from lp.variables.min_key_value import calculate_min_k_value
from lp.variables.same_neighborhood_covering import add_neighborhood_variables


def create_variables(parameters: Parameters):
    number_of_covered_neighborhood = 0
    variables_dictionary: dict[int, tuple[int, int]] = {}

    # adjacency matrix rules
    add_adjacency_matrix_variables(parameters, variables_dictionary)
    # neighborhood rules
    number_of_covered_neighborhood += add_neighborhood_variables(parameters, variables_dictionary)

    variables = {}
    for index, r in variables_dictionary.items():
        if parameters.with_fractional_results:
            variables[index] = parameters.solver.NumVar(r[0], r[1], '%i' % index)
        else:
            variables[index] = parameters.solver.IntVar(r[0], r[1], '%i' % index)

    # Add k as a variable to the end of list
    min_k = calculate_min_k_value(parameters)
    max_k = parameters.b_len if parameters.prices is None else sys.maxsize
    if parameters.with_fractional_results:
        variables[len(variables_dictionary)] = parameters.solver.NumVar(
            min_k, max_k, '%i' % (len(variables_dictionary))
        )
    else:
        variables[len(variables_dictionary)] = parameters.solver.IntVar(
            min_k, max_k, '%i' % (len(variables_dictionary))
        )
    parameters.set_variables(variables)
    return number_of_covered_neighborhood
