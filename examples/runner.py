import os
import time
import networkx as nx
import matplotlib.pyplot as plt

from graph_generator.bipartite_corrector import extract_nodes
from graph_generator.bipartite_transformer import transform_bigraph
from utility import utils
from lp.solver import Solver
from lp.solver import Parameters
from lp.solver import Solution
import numpy as np


def print_values(values, l_len):
    value_numbers = set()
    print(f"fractional_values:")
    for index, val in values.items():
        if index % l_len == 0:
            print()
        val = np.round(val, 3)
        value_numbers.add(val)
        print(f"X{utils.from_index(l_len, index)}: {val}", end=", ")
    print()
    print(f"Numbers: {value_numbers}")


def __solve(g, b_len, s_len, mapped_prices, fractional) -> Solution:
    start = time.time()
    parameters = Parameters(g, b_len, s_len, fractional, mapped_prices)
    result = Solver(parameters).solve()
    running_time = time.time() - start
    result.set_solution_time(running_time)
    return result


def run(edge_list, prices, draw_graph=False, values_in_console=False):
    g, b, s = utils.create_bipartite_graph(edge_list)
    b_len = len(b)
    s_len = len(s)

    if draw_graph:
        fig, ax = plt.subplots(figsize=(b_len * 1.25, b_len * (b_len / s_len) * 2))
        pos = nx.bipartite_layout(g, b)
        nx.draw(g, pos=pos, node_size=2000, with_labels=True, node_color=["red"] * b_len + ["green"] * s_len)
        plt.show()

    g, b, s = extract_nodes(g, b)
    g, b, s, b_len, s_len, edge_mapper = transform_bigraph(g)
    mapped_prices = None if prices is None else {edge_mapper[k]: v for k, v in prices.items()}
    integer_solution = __solve(g, b_len, s_len, mapped_prices, False)
    fractional_solution = __solve(g, b_len, s_len, mapped_prices, True)
    if values_in_console:
        print_values(fractional_solution.values, b_len + s_len)
    print(f"number_of_twins:{integer_solution.number_of_twins}")
    print(f"number_of_covered_neighborhood:{integer_solution.number_of_covered_neighborhood}")
    print(f"sequence: [", end="")
    edge_mapper = {v: k for k, v in edge_mapper.items()}
    for seq in integer_solution.sequence:
        print(f"{edge_mapper[seq]}, ", end="")
    print("]")
    print(f"integral_result: [{integer_solution.k}]")
    print(f"fractional_result: [{fractional_solution.k}]")
    print(f"running_time:{integer_solution.solution_time}")
    print(f"running_time:{fractional_solution.solution_time}")


if __name__ == '__main__':
    example_number = input("Which example do you want to run (enter the number only)?")
    # B to S edge list
    with open(f'{example_number}.txt') as f:
        edge_list = [tuple(map(str.strip, i.split(','))) for i in f]

    prices = None
    if os.path.exists(f'{example_number}-prices.txt'):
        with open(f'{example_number}-prices.txt') as f:
            prices = {int(i.split('=')[0].strip()): int(i.split('=')[1].strip()) for i in f}
    run(edge_list, prices, True)
