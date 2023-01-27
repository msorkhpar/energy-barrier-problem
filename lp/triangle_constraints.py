from lp.utils import to_index


def add_triangle_constraints(solver, variables, l):
    l_len = len(l)
    for i in l:
        for j in l:
            if i == j:
                continue

            for k in l:
                if k == i or k == j:
                    continue

                solver.Add(variables[to_index(l_len, i, j)] +
                           variables[to_index(l_len, j, k)] +
                           variables[to_index(l_len, k, i)] >= 1)
