from utility.utils import to_index


def add_degree_twos_constraints(solver, variables, g, s):
    def has_at_least_one_neighbor(v1, v2):
        for n in g[v1]:
            if n in g[v2]:
                return True
        return False

    p = sorted([int(node) for node in g.nodes() if g.degree(node) == 2 and g.nodes[node]['bipartite'] == 1])
    p_set = set(p)

    for i in p:
        for j in p:
            if j <= i or not has_at_least_one_neighbor(i, j):
                continue

            for k in s:
                if k == i or k == j or g.degree(k) == 1:
                    continue
                if k not in p_set:
                    solver.Add(variables[to_index(i, j)] <= variables[to_index(j, k)])
                elif j < k:
                    solver.Add(variables[to_index(i, j)] <= variables[to_index(j, k)])
    del p, p_set
