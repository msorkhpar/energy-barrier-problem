from functools import reduce

from lp.solver import Parameters


def calculate_min_k_value(parameters: Parameters):
    # find min degree of nodes in S
    return reduce(
        min, map(
            lambda node: parameters.g.degree[node], filter(
                lambda node: parameters.g.nodes[node]['bipartite'] == 1, parameters.g.nodes()
            )
        )
    )
