from utility.utils import to_index, print_value


def add_degree_ones_variables(variables_dictionary, g, b, l):
    # degree on nodes
    processed_vb = set()
    processed_nvb = set()
    for vb in b:
        has_degree_one_neighbor = False
        for nvb in g[vb]:
            if g.degree(nvb) != 1:
                continue
            has_degree_one_neighbor = True
            for vl in l:
                if vl == vb or vl == nvb or vl in processed_nvb or vl in processed_vb:
                    continue
                variables_dictionary.update({to_index(vb, vl): (1, 1)})
                print_value(vb, vl, 1, 1)
                variables_dictionary.update({to_index(vl, vb): (0, 0)})
                print_value(vl, vb, 0, 0)
                variables_dictionary.update({to_index(nvb, vl): (1, 1)})
                print_value(nvb, vl, 1, 1)
                variables_dictionary.update({to_index(vl, nvb): (0, 0)})
                print_value(vl, nvb, 0, 0)

            variables_dictionary.update({to_index(vb, nvb): (1, 1)})
            print_value(vb, nvb, 1, 1)
            variables_dictionary.update({to_index(nvb, vb): (0, 0)})
            print_value(nvb, vb, 0, 0)
            processed_nvb.add(nvb)
        if has_degree_one_neighbor:
            processed_vb.add(vb)
    del processed_vb, processed_nvb