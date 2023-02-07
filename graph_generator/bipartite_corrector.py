def get_tuple(node_name):
    node_type = type(node_name)
    if node_type is int or node_type is float:
        return node_name
    if node_type is str and "," not in node_name:
        return int(node_name)
    return tuple(map(int, node_name[2:-1].split(',')))


def __omit_degree_ones(g, b):
    reserved_energy = 0
    processed_vb = set()
    for vb in b:
        for nvb in g[vb]:
            if g.degree(nvb) == 1:
                processed_vb.add(vb)
                reserved_energy += 1
    reserved_energy = reserved_energy - len(processed_vb)

    nodes_to_remove = [node for node, degree in g.degree() if degree < 2 and g.nodes[node]['bipartite'] == 1]
    if nodes_to_remove:
        print(f"Removing {nodes_to_remove} nodes from the graph")
        g.remove_nodes_from(nodes_to_remove)
    return g, reserved_energy


def extract_nodes(g, b):
    g, reserved_energy = __omit_degree_ones(g, b)
    # print(f"Reserved energy after removing degree ones: {reserved_energy}")

    b = sorted([get_tuple(n) for n in g.nodes if g.nodes[n]['bipartite'] == 0])
    s = sorted([get_tuple(n) for n in g.nodes if g.nodes[n]['bipartite'] == 1])
    return g, b, s
