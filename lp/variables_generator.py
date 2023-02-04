from lp.utils import to_index


def __is_fully_covered(g, v1, v2):
    if g.degree(v1) == 0:
        return False
    for n_v2 in g[v2].keys():
        if g.degree(v2) == 0:
            continue
        if g[v1].get(n_v2) is None:
            return False
    return True


def create_variables(solver, g, b, s, l, with_fractional_results):
    variables = {}
    number_of_covered_neighborhood = 0
    b_len = len(b)
    vars_dict = {}

    # adjacency matrix rules
    for i in l:
        for j in l:
            index = to_index(i, j)
            if i == j:
                vars_dict.update({index: (1, 1)})
            elif i < b_len and j >= b_len and int(g.has_edge(i, j)) == 1:
                # if there is an edge from i to j then X[i,j] = 1
                vars_dict.update({index: (1, 1)})
            else:
                # create the rest of variables with 0 <= X[i,j] <= 1 range
                vars_dict.update({index: (0, 1)})

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

    # degree on nodes
    processed_vb = set()
    processed_nvb = set()
    for vb in b:
        has_degree_one_neighbor = False
        for nvb in g[vb]:
            if g.degree(nvb) != 1:
                continue
            has_degree_one_neighbor = True
            for vl in l:
                if vl == vb or vl == nvb or vl in processed_nvb or vl in processed_vb:
                    continue
                vars_dict.update({to_index(vb, vl): (1, 1)})
                vars_dict.update({to_index(vl, vb): (0, 0)})
                vars_dict.update({to_index(nvb, vl): (1, 1)})
                vars_dict.update({to_index(vl, nvb): (0, 0)})
            vars_dict.update({to_index(vb, nvb): (1, 1)})
            vars_dict.update({to_index(nvb, vb): (0, 0)})
            processed_nvb.add(nvb)
        if has_degree_one_neighbor:
            processed_vb.add(vb)
    del processed_vb, processed_nvb

    for index, r in vars_dict.items():
        if with_fractional_results:
            variables[index] = solver.NumVar(r[0], r[1], '%i' % index)
        else:
            variables[index] = solver.IntVar(r[0], r[1], '%i' % index)

    # Add k as a variable to the end of list
    if with_fractional_results:
        variables[len(vars_dict)] = solver.NumVar(1, b_len, '%i' % (len(vars_dict)))
    else:
        variables[len(vars_dict)] = solver.IntVar(1, b_len, '%i' % (len(vars_dict)))

    return variables, number_of_covered_neighborhood
