from lp.solver import Parameters


def add_adjacency_matrix_variables(parameters: Parameters, variables_dictionary: dict[int, tuple[int, int]]):
    # adjacency matrix rules
    for i in parameters.l:
        for j in parameters.l:
            index = parameters.to_index(i, j)
            if i == j:
                variables_dictionary.update({index: (1, 1)})
            elif i < parameters.b_len and j >= parameters.b_len and int(parameters.g.has_edge(i, j)) == 1:
                # if there is an edge from i to j then X[i,j] = 1
                variables_dictionary.update({index: (1, 1)})

            else:
                # create the rest of variables with 0 <= X[i,j] <= 1 range
                variables_dictionary.update({index: (0, 1)})
