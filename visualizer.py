#!/usr/bin/env python3

import os

from lp.solver import Solver
from lp.solver import Parameters
from persistent import retrieve_service
import networkx as nx
from matplotlib import pyplot as plt

from utility import utils
from graph_generator.bipartite_corrector import extract_nodes
from graph_generator.bipartite_transformer import transform_bigraph


# matplotlib.use('TkAgg')


def sequence_validity(sample):
    _sequence = sample['sequence']
    _prices = sample['prices']
    _k = sample['integer_k']
    _G, _b, _s = utils.create_bipartite_graph(sample['edges'])

    if len(_sequence) != len(_b) + len(_s):
        print("Invalid sequence!")
        print(f"Sequence length is not equal to the number of nodes in the graph!")
        return
    for turn in _sequence:
        if turn in _b:
            k = _k - (1 if _prices is None else _prices[turn])
            _G.remove_node(turn)
        elif turn in _s:
            if _G.degree(turn) == 0:
                k = _k + (1 if _prices is None else _prices[turn])
                _G.remove_node(turn)
            else:
                print("Invalid sequence!")
                print(f"Attempting to remove a node with degree > 0 from S side => node:[{turn}]")
                return
        else:
            print("Invalid sequence!")
            print(f"Given edge[{turn}] is not a part of the graph!!")
            return
        if k < 0:
            print("Invalid sequence!")
            print(f"K become negative by removing [{turn}] Not a valid sequence")
            return
    print("Sequence is valid!")


if __name__ == '__main__':
    bigraph_db_id = input("Enter bgraph DB id: ")
    sample = retrieve_service.retrieve_sample(bigraph_db_id)
    G, b, s = utils.create_bipartite_graph(sample['edges'])
    b_len = len(b)
    s_len = len(s)
    g_len = len(sample['edges'])
    print(f"|b|: {b_len}, |s|: {s_len}, |g|: {g_len}")

    print()
    print(f"edges:{sample['edges']}")
    print(f"sequence: {sample['sequence']}")
    print(f"prices: {sample['prices']}")
    sequence_validity(sample)
    print()
    fig, ax = plt.subplots(figsize=(b_len, b_len * (b_len / s_len) * 1.5))

    pos = nx.bipartite_layout(G, sample['b'])
    nx.draw(G, pos=pos, node_size=2000, with_labels=True,
            node_color=["red"] * b_len + ["green"] * s_len)
    plt.show()

    prices = sample['prices'] if os.environ.get('DB_HOST') == "True" else None
    parameters = Parameters(G, b_len, s_len, True, prices)
    fractional_result = Solver(parameters).solve()
    print(f"[ {bigraph_db_id} ] of {os.environ.get('DB_NAME').upper()}")
    print("*" * 40)
    print(f"from DB fractional result: [{sample['fractional_k']}]")
    print(f"fresh solving fractional result: [{fractional_result.k}]")
    print("*" * 40)
    parameters.with_fractional_results = False
    integer_result = Solver(parameters).solve()
    print("*" * 40)
    print(f"from DB integer result: [{sample['integer_k']}]")
    print(f"fresh solving integer result: [{integer_result.k}]")
    print("*" * 40)
