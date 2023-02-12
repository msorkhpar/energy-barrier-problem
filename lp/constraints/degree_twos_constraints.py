from lp.parameters import Parameters


def add_degree_twos_constraints(parameters: Parameters):
    def __has_at_least_one_neighbor(v1, v2):
        for n in parameters.g[v1]:
            if n in parameters.g[v2]:
                return True
        return False

    p = sorted([
        int(node) for node in parameters.g.nodes() if parameters.g.degree(node) == 2 and parameters.g.nodes[node]['bipartite'] == 1
    ])
    p_set = set(p)

    for i in p:
        for j in p:
            if j <= i or not __has_at_least_one_neighbor(i, j):
                continue

            for k in parameters.s:
                if k == i or k == j:
                    continue
                if (k not in p_set) or j < k:
                    parameters.add_constraint(parameters.var(i, j) <= parameters.var(j, k))

    del p, p_set
