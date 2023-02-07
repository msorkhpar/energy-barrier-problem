import time
import networkx as nx
import matplotlib.pyplot as plt

from graph_generator.bipartite_corrector import extract_nodes
from graph_generator.bipartite_transformer import transform_bigraph
from utility import utils
from lp.solver import solve
import numpy as np


def __solve(g, b_len, s_len, fractional):
    start = time.time()
    result = solve(g, b_len, s_len, fractional)
    running_time = time.time() - start
    result["running_time"] = running_time
    return result


def run(draw_graph=False):
    g, b, s = utils.create_random_bipartite_graph(7, 10, 30)
    b_len = len(b)
    s_len = len(s)

    if draw_graph:
        fig, ax = plt.subplots(figsize=(b_len * 1.25, b_len * (b_len / s_len) * 2))
        pos = nx.bipartite_layout(g, b)
        nx.draw(g, pos=pos, node_size=2000, with_labels=True, node_color=["red"] * b_len + ["green"] * s_len)
        plt.show()

    g, b, s = extract_nodes(g, b)
    utils.set_l_len(b_len + s_len)
    g, b, s, b_len, s_len, edge_mapper = transform_bigraph(g)

    integer_solution = __solve(g, b_len, s_len, False)
    fractional_solution = __solve(g, b_len, s_len, True)
    print(f"number_of_twins:{integer_solution['number_of_twins']}")
    print(f"number_of_covered_neighborhood:{integer_solution['number_of_covered_neighborhood']}")
    print(f"sequence: [", end="")
    edge_mapper = {v: k for k, v in edge_mapper.items()}
    for seq in integer_solution['sequence']:
        print(f"{edge_mapper[seq]}, ", end="")
    print("]")
    print(f"integral_result: [{integer_solution['k']}]")
    print(f"fractional_result: [{fractional_solution['k']}]")
    print(f"running_time:{integer_solution['running_time']}")
    print(f"running_time:{fractional_solution['running_time']}")


if __name__ == '__main__':
    run(True)
