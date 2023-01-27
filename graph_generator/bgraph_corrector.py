def get_tuple(node_name):
    return tuple(map(int, node_name[2:-1].split(',')))


def omit_degree_ones_from_bgraph(g):
    g.remove_nodes_from([node for node, degree in g.degree() if degree < 2])

    b = sorted([get_tuple(n) for n in g.nodes if g.nodes[n]['bipartite'] == 0])
    s = sorted([get_tuple(n) for n in g.nodes if g.nodes[n]['bipartite'] == 1])

    return g, b, s
