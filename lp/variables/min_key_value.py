import sys
from functools import reduce
import numpy as np
from lp.solver import Parameters


def calculate_min_k_value(parameters: Parameters):
    min_node_id = -1
    min_value = sys.maxsize
    min_k = 0
    # find the node with min degree on S
    for node in [node for node in parameters.g.nodes() if parameters.g.nodes[node]['bipartite'] == 1]:
        degree = parameters.g.degree[node]
        if degree < min_value:
            min_value = degree
            min_node_id = node

    # Iterate over neighbors of min degree of S and sum their prices
    for neighbor in parameters.g.neighbors(min_node_id):
        min_k += 1 if parameters.prices is None else parameters.prices[neighbor]

    return min_k
