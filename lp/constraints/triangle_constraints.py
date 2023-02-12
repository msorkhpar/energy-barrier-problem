from lp.parameters import Parameters


def add_triangle_constraints(parameters: Parameters):
    for i in parameters.l:
        for j in parameters.l:
            if i == j:
                continue

            for k in parameters.l:
                if k == i or k == j:
                    continue
                parameters.add_constraint(parameters.var(i, j) + parameters.var(j, k) + parameters.var(k, i) >= 1)
