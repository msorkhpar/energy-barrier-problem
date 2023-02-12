from datetime import datetime
import networkx as nx
from networkx.algorithms import bipartite


def to_index(l_len, i, j):
    return i * l_len + j


def from_index(l_len, index):
    index = int(index)
    if index == l_len ** 2:
        return "K", ""
    return index // l_len, index % l_len


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_bipartite_graph(edge_list: list[tuple[int, int]]):
    g = nx.Graph()
    b = set()
    s = set()
    edges = list()
    for source, target in edge_list:
        b.add(int(source))
        s.add(int(target))
        edges.append((int(source), int(target)))

    g.add_nodes_from([node for node in sorted(b)], bipartite=0)
    g.add_nodes_from([node for node in sorted(s)], bipartite=1)
    g.add_edges_from(sorted(edges))

    return g, b, s


def create_complete_bipartite_graph(n1, n2):
    g = nx.complete_bipartite_graph(n1, n2)
    b = [node for node, degree in g.degree() if g.nodes[node]['bipartite'] == 0]
    s = [node for node, degree in g.degree() if g.nodes[node]['bipartite'] == 1]

    return g, b, s


def create_random_bipartite_graph(b, s, e):
    g = bipartite.gnmk_random_graph(b, s, e)
    b = [node for node, degree in g.degree() if g.nodes[node]['bipartite'] == 0]
    s = [node for node, degree in g.degree() if g.nodes[node]['bipartite'] == 1]

    return g, b, s
