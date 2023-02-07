from datetime import datetime
import networkx as nx
from networkx.algorithms import bipartite

l_len = 0
print_values = False


def set_l_len(__l_len):
    global l_len
    l_len = __l_len


def enable_print_values():
    global print_values
    print_values = True

def to_index(i, j):
    return i * l_len + j


def from_index(index):
    index = int(index)
    if index == l_len ** 2:
        return "K", ""
    return index // l_len, index % l_len


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def print_value(i, j, lb, ub):
    global print_values
    if print_values:
        if lb == ub:
            print(f"X({i}_{j}) = {lb}")
        else:
            print(f"{lb} <= X({i}_{j}) <= {ub}")


def print_value_sign(v1, v2, v3, v4, sign):
    global print_values
    if print_values:
        print(f"X({v1}_{v2}) {sign} X({v3}_{v4})")


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
