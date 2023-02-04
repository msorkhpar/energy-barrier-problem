from utility.utils import to_index


def add_flipper_constraints(solver, variables, l):
    for i in l:
        for j in l:
            if i == j:
                continue
            solver.Add(variables[to_index(i, j)] + variables[to_index(j, i)] == 1)
