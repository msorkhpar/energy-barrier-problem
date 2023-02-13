from lp.parameters import Parameters


def add_flipper_constraints(parameters: Parameters):
    for i in parameters.l:
        for j in parameters.l:
            if i == j:
                continue
            parameters.add_constraint(parameters.var(i, j) + parameters.var(j, i) == 1)
