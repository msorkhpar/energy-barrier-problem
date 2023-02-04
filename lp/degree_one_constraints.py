from lp.utils import to_index, from_index


def add_degree_one_constraints(solver, variables, g, b, l):
    # degree on nodes
    degree_one_candidates = set()
    processed_nvb = set()
    for vb in b:
        has_degree_one_neighbor = False
        for nvb in g[vb]:
            if g.degree(nvb) != 1:
                continue
            has_degree_one_neighbor = True
            for vl in l:
                if vl == vb or vl == nvb or vl in processed_nvb or vl in degree_one_candidates:
                    continue
                solver.Add(variables[to_index(vb, vl)] == 1)
                solver.Add(variables[to_index(nvb, vl)] == 1)
            solver.Add(variables[to_index(vb, nvb)] == 1)
            processed_nvb.add(nvb)
        if has_degree_one_neighbor:
            degree_one_candidates.add(vb)
