import random
import networkx as nx
from utility.utils import create_random_bipartite_graph


def generate_random_bigraph(b_size: int, s_size: int, min_no_edges: int, max_no_edges):
    g, b, s = create_random_bipartite_graph(b_size, s_size, random.randint(min_no_edges, max_no_edges))
    g.add_nodes_from([node for node in b], bipartite=0)
    g.add_nodes_from([node for node in s], bipartite=1)

    return g, b, s
