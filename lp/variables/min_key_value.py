from functools import reduce


def calculate_min_k_value(g):
    # find min degree of nodes in S
    return reduce(
        min, map(
            lambda node: g.degree[node], filter(
                lambda node: g.nodes[node]['bipartite'] == 1, g.nodes()
            )
        )
    )
