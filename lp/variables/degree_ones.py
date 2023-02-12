from lp.solver import Parameters


def add_degree_ones_variables(parameters: Parameters, variables_dictionary: dict[int, tuple[int, int]]):
    # degree on nodes
    processed_vb = set()
    processed_nvb = set()
    for vb in parameters.b:
        has_degree_one_neighbor = False
        for nvb in parameters.g[vb]:
            if parameters.g.degree(nvb) != 1:
                continue
            has_degree_one_neighbor = True
            for vl in parameters.l:
                if vl == vb or vl == nvb or vl in processed_nvb or vl in processed_vb:
                    continue
                variables_dictionary.update({parameters.to_index(vb, vl): (1, 1)})
                variables_dictionary.update({parameters.to_index(vl, vb): (0, 0)})
                variables_dictionary.update({parameters.to_index(nvb, vl): (1, 1)})
                variables_dictionary.update({parameters.to_index(vl, nvb): (0, 0)})

            variables_dictionary.update({parameters.to_index(vb, nvb): (1, 1)})
            variables_dictionary.update({parameters.to_index(nvb, vb): (0, 0)})
            processed_nvb.add(nvb)
        if has_degree_one_neighbor:
            processed_vb.add(vb)
    del processed_vb, processed_nvb
