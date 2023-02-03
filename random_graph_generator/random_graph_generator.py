import random
import networkx as nx


def generate_random_bigraph(max_allowed_nodes: int, max_allowed_edges: int, min_allowed_edges: int = None):
    if min_allowed_edges is None:
        min_allowed_edges = min(max_allowed_edges, max_allowed_nodes)
    if min_allowed_edges > max_allowed_edges:
        min_allowed_edges, max_allowed_edges = max_allowed_edges, min_allowed_edges

    b = list(range(max_allowed_nodes))
    s = list(range(max_allowed_nodes, max_allowed_nodes * 2))
    no_edges = random.randint(min_allowed_edges, max_allowed_edges)
    edges = [(random.choice(b), random.choice(s)) for _ in range(no_edges)]
    g = nx.Graph()
    g.add_nodes_from([node for node in b], bipartite=0)
    g.add_nodes_from([node for node in s], bipartite=1)
    g.add_edges_from(edges)

    return g, b, s
