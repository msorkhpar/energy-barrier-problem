import networkx as nx


def decompose_graph(graph, b_len, s_len):
    adj_list = nx.to_dict_of_lists(graph)

    edge_set = set(nx.generate_edgelist(graph, delimiter='_', data=False))

    return adj_list, edge_set
