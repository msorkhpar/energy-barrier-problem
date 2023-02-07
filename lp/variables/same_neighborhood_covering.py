from utility.utils import to_index, print_value


def __is_fully_covered(g, v1, v2):
    if g[v1] == g[v2]:
        return False
    for n_v2 in g[v2].keys():
        if g[v1].get(n_v2) is None:
            return False
    return True


def add_neighborhood_variables(variables_dictionary, g, b, s):
    number_of_covered_neighborhood = 0
    # neighborhood rules from B side
    for v1 in b:
        for v2 in b:
            if v1 == v2:
                continue
            if __is_fully_covered(g, v1, v2):
                number_of_covered_neighborhood += 1
                variables_dictionary.update({to_index(v1, v2): (1, 1)})
                print_value(v1, v2, 1, 1)
                variables_dictionary.update({to_index(v2, v1): (0, 0)})
                print_value(v2, v1, 0, 0)

    # neighborhood rules from S side
    for v1 in s:
        for v2 in s:
            if v1 == v2:
                continue
            if __is_fully_covered(g, v1, v2):
                number_of_covered_neighborhood += 1
                variables_dictionary.update({to_index(v1, v2): (0, 0)})
                print_value(v1, v2, 0, 0)
                variables_dictionary.update({to_index(v2, v1): (1, 1)})
                print_value(v2, v1, 1, 1)

    return number_of_covered_neighborhood
