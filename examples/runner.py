import time
import networkx as nx
import matplotlib.pyplot as plt

from graph_generator.bipartite_corrector import extract_nodes
from graph_generator.bipartite_transformer import transform_bigraph
from utility import utils
from lp.solver import solve
import numpy as np


def print_values(values, l_len):
    value_numbers = set()
    for index, val in values.items():
        if index % l_len == 0:
            print()
        val = np.round(val, 3)
        value_numbers.add(val)
        print(f"X{utils.from_index(index)}: {val}", end=", ")
    print()
    print(f"Numbers: {value_numbers}")


def __create_bipartite_graph(edge_list: list[tuple[int, int]]):
    g = nx.Graph()
    b = set()
    s = set()
    edges = list()
    for source, target in edge_list:
        b.add(source)
        s.add(target)
        edges.append((source, target))

    g.add_nodes_from([node for node in b], bipartite=0)
    g.add_nodes_from([node for node in s], bipartite=1)
    g.add_edges_from(edges)

    return g, b, s


def __solve(g, b_len, s_len, fractional):
    start = time.time()
    result = solve(g, b_len, s_len, fractional, 8)
    running_time = time.time() - start
    result["running_time"] = running_time
    return result


def run(edge_list):
    g, b, s = __create_bipartite_graph(edge_list)
    b_len = len(b)
    s_len = len(s)
    fig, ax = plt.subplots(figsize=(b_len, b_len * (b_len / s_len) * 2))

    pos = nx.bipartite_layout(g, b)
    nx.draw(g, pos=pos, node_size=2000, with_labels=True,
            node_color=["red"] * b_len + ["green"] * s_len)
    plt.show()
    g, b, s = extract_nodes(g)
    g, b_len, s_len, edge_mapper = transform_bigraph(g)
    utils.set_l_len(b_len + s_len)

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
    print(f"fractional_values:")
    # print_values(fractional_solution['values'], b_len + s_len)


if __name__ == '__main__':
    example_number = input("Which example do you want to run (enter the number only)?")
    # B to S edge list
    with open(f'{example_number}.txt') as f:
        edge_list = [tuple(map(str.strip, i.split(','))) for i in f]
    run(edge_list)
