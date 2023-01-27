from lp.utils import to_index


def __add_twins(side, solver, variables, g, l):
    l_len = len(l)
    processed = set()
    twins_counter = 0
    for va in side:
        for vb in side:
            if va == vb or vb in processed:
                continue
            if g[vb] == g[va]:
                for vc in l:
                    if g[vc] == g[va] or vc == va or vc == vb:
                        continue
                    x_ac = to_index(l_len, va, vc)
                    x_bc = to_index(l_len, vb, vc)
                    solver.Add(variables[x_ac] == variables[x_bc])
                twins_counter += 1
        processed.add(va)
        return twins_counter


def set_twin_nodes_constraints(solver, variables, g, b, s, l):
    twins_counter = 0
    twins_counter += __add_twins(b, solver, variables, g, l)
    twins_counter += __add_twins(s, solver, variables, g, l)
    return twins_counter
