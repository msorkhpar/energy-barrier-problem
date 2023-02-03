from lp.utils import to_index


def add_triangle_constraints(solver, variables, l):
    for i in l:
        for j in l:
            if i == j:
                continue

            for k in l:
                if k == i or k == j:
                    continue

                solver.Add(variables[to_index(i, j)] +
                           variables[to_index(j, k)] +
                           variables[to_index(k, i)] >= 1)
