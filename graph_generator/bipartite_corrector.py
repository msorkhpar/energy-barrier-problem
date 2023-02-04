def get_tuple(node_name):
    node_type = type(node_name)
    if node_type is int or node_type is float:
        return node_name
    if node_type is str and "," not in node_name:
        return node_name
    return tuple(map(int, node_name[2:-1].split(',')))


def __omit_degree_ones(g):
    nodes_to_remove = [node for node, degree in g.degree() if degree < 2 and g.nodes[node]['bipartite'] == 1]
    if nodes_to_remove:
        print(f"Removing {len(nodes_to_remove)} nodes from s")
        g.remove_nodes_from(nodes_to_remove)

    return g


def extract_nodes(g):
    g = __omit_degree_ones(g)
    b = sorted([get_tuple(n) for n in g.nodes if g.nodes[n]['bipartite'] == 0])
    s = sorted([get_tuple(n) for n in g.nodes if g.nodes[n]['bipartite'] == 1])
    return g, b, s
