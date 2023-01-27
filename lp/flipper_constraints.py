from lp.utils import to_index


def add_flipper_constraints(solver, variables, l):
    l_len = len(l)
    for i in l:
        for j in l:
            if i == j:
                continue
            solver.Add(variables[to_index(l_len, i, j)] + variables[to_index(l_len, j, i)] == 1)