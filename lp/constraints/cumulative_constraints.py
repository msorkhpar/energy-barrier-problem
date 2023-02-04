from utility.utils import to_index, from_index


def add_cumulative_constraints(solver, variables, b, s, l):
    l_len = len(l)
    for m in l:

        row = [0] * (l_len ** 2 + 1)
        row[l_len ** 2] = 1
        constraint = solver.Constraint(0, l_len)

        for i in b:
            if i != m:
                row[to_index(i, m)] = -1

        for j in s:
            if j != m:
                row[to_index(j, m)] = 1
        for tmp_i in range(l_len ** 2 + 1):
            i_index, j_index = from_index(tmp_i)
            if i_index == j_index:
                row[tmp_i] = 0
            constraint.SetCoefficient(variables[tmp_i], row[tmp_i])
