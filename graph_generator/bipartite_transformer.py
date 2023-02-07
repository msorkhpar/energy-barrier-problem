import networkx as nx

from utility.utils import set_l_len


def transform_bigraph(g):
    left_nodes = [n for n in g.nodes if g.nodes[n]['bipartite'] == 0]
    right_nodes = [n for n in g.nodes if g.nodes[n]['bipartite'] == 1]
    b_len = 0
    s_len = 0
    edge_mapper = dict()

    i = 0
    for node in left_nodes:
        if g.degree[node] == 0:
            g.remove_node(node)
            continue
        edge_mapper.update({node: i})
        b_len += 1
        i += 1
    for node in right_nodes:
        if g.degree[node] == 0:
            g.remove_node(node)
            continue
        edge_mapper.update({node: i})
        s_len += 1
        i += 1

    g = nx.relabel_nodes(g, edge_mapper)
    edge_mapper = dict(sorted(edge_mapper.items(), key=lambda x: x[1]))
    set_l_len(s_len + b_len)
    b = list(range(b_len))
    s = list(range(b_len, s_len + b_len))
    return g, b, s, b_len, s_len, edge_mapper
