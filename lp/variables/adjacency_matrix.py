from utility.utils import to_index


def add_adjacency_matrix_variables(vars_dict, g, b, l):
    b_len = len(b)
    # adjacency matrix rules
    for i in l:
        for j in l:
            index = to_index(i, j)
            if i == j:
                vars_dict.update({index: (1, 1)})
            elif i < b_len and j >= b_len and int(g.has_edge(i, j)) == 1:
                # if there is an edge from i to j then X[i,j] = 1
                vars_dict.update({index: (1, 1)})
            else:
                # create the rest of variables with 0 <= X[i,j] <= 1 range
                vars_dict.update({index: (0, 1)})
