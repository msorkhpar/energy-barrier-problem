import networkx as nx


def transform_bgraph(g):
    left_nodes = [n for n in g.nodes if g.nodes[n]['bipartite'] == 0]
    right_nodes = [n for n in g.nodes if g.nodes[n]['bipartite'] == 1]
    b_len = 0
    s_len = 0
    edge_mapper = dict()

    i = 0
    for node in left_nodes:
        if g.degree[node] == 0:
            continue
        edge_mapper.update({node: i})
        b_len += 1
        i += 1
    for node in right_nodes:
        if g.degree[node] == 0:
            continue
        edge_mapper.update({node: i})
        s_len += 1
        i += 1

    g = nx.relabel_nodes(g, edge_mapper)
    edge_mapper = dict(sorted(edge_mapper.items(), key=lambda x: x[1]))

    return g, b_len, s_len, edge_mapper
