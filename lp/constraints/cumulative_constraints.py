import sys

from lp.parameters import Parameters


def add_cumulative_constraints(parameters: Parameters):
    upper_bound = parameters.l_len if parameters.prices is None else sys.maxsize
    for m in parameters.l:
        row = [0] * (parameters.l_len ** 2 + 1)
        # coefficient of the k should be set to 1
        row[parameters.l_len ** 2] = 1
        constraint = parameters.solver.Constraint(0, upper_bound)

        for i in parameters.b:
            if i != m:
                value = -1 if parameters.prices is None else -1 * parameters.prices[i]
                row[parameters.to_index(i, m)] = value

        for j in parameters.s:
            if j != m:
                value = 1 if parameters.prices is None else parameters.prices[j]
                row[parameters.to_index(j, m)] = value

        for tmp_i in range(parameters.l_len ** 2 + 1):
            i_index, j_index = parameters.from_index(tmp_i)
            if i_index == j_index:
                row[tmp_i] = 0
            constraint.SetCoefficient(parameters.variables[tmp_i], row[tmp_i])