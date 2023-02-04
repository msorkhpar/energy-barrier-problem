#!/usr/bin/env python3

from persistent import retrieve_service
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib


# matplotlib.use('TkAgg')


def create_bipartite_of_intersections_inner(edge_list: list[tuple[int, int]], b, s):
    G = nx.Graph()
    G.add_nodes_from(b, bipartite=0)
    G.add_nodes_from(s, bipartite=1)
    G.add_edges_from(edge_list)

    return G, len(b), len(s)


if __name__ == '__main__':
    bigraph_db_id = input("Enter bgraph DB id: ")
    sample = retrieve_service.retrieve_sample(bigraph_db_id)
    B, b_len, s_len = create_bipartite_of_intersections_inner(sample['edges'], sample['b'], sample['s'])

    print()
    print(f"b: {b_len}, s: {s_len}")
    print(f"integer result: [{sample['integer_k']}]")
    print(f"fractional result: [{sample['fractional_k']}]")
    print(f"edges:{sample['edges']}")
    print(f"sequence: {sample['sequence']}")

    fig, ax = plt.subplots(figsize=(b_len, b_len * (b_len / s_len)))

    pos = nx.bipartite_layout(B, sample['b'])
    nx.draw(B, pos=pos, node_size=2000, with_labels=True,
            node_color=["red"] * b_len + ["green"] * s_len)
    plt.show()
