from lp.solver import Parameters


def __is_fully_covered(g, v1, v2):
    if g[v1] == g[v2]:
        return False
    for n_v2 in g[v2].keys():
        if g[v1].get(n_v2) is None:
            return False
    return True


def add_neighborhood_variables(parameters: Parameters, variables_dictionary):
    number_of_covered_neighborhood = 0
    # neighborhood rules from B side
    for v1 in parameters.b:
        for v2 in parameters.b:
            if v1 == v2:
                continue
            if __is_fully_covered(parameters.g, v1, v2):
                number_of_covered_neighborhood += 1
                variables_dictionary.update({parameters.to_index(v1, v2): (1, 1)})
                variables_dictionary.update({parameters.to_index(v2, v1): (0, 0)})

    # neighborhood rules from S side
    for v1 in parameters.s:
        for v2 in parameters.s:
            if v1 == v2:
                continue
            if __is_fully_covered(parameters.g, v1, v2):
                number_of_covered_neighborhood += 1
                variables_dictionary.update({parameters.to_index(v1, v2): (0, 0)})
                variables_dictionary.update({parameters.to_index(v2, v1): (1, 1)})

    return number_of_covered_neighborhood
