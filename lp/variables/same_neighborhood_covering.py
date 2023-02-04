from utility.utils import to_index


def __is_fully_covered(g, v1, v2):
    if g.degree(v1) == 0:
        return False
    for n_v2 in g[v2].keys():
        if g.degree(v2) == 0:
            continue
        if g[v1].get(n_v2) is None:
            return False
    return True


def add_neighborhood_variables(vars_dict, g, b, s):
    number_of_covered_neighborhood = 0
    # neighborhood rules from B side
    for v1 in b:
        for v2 in b:
            if v1 == v2:
                continue
            if __is_fully_covered(g, v1, v2):
                number_of_covered_neighborhood += 1
                vars_dict.update({to_index(v1, v2): (1, 1)})
                vars_dict.update({to_index(v2, v1): (0, 0)})

    # neighborhood rules from S side
    for v1 in s:
        for v2 in s:
            if v1 == v2:
                continue
            if __is_fully_covered(g, v1, v2):
                number_of_covered_neighborhood += 1
                vars_dict.update({to_index(v1, v2): (0, 0)})
                vars_dict.update({to_index(v2, v1): (1, 1)})
    return number_of_covered_neighborhood
