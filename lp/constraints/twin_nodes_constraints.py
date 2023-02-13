from lp.parameters import Parameters


def __add_twins(side, parameters: Parameters):
    processed = set()
    twins_counter = 0
    for va in side:
        for vb in side:
            if va == vb or vb in processed:
                continue
            if parameters.g[vb] == parameters.g[va]:
                if va < vb:
                    parameters.add_constraint(parameters.var(va, vb) == 1)

                for vc in parameters.l:
                    if parameters.g[vc] == parameters.g[va] or vc == va or vc == vb:
                        continue
                    parameters.add_constraint(parameters.var(va, vc) == parameters.var(vb, vc))
                twins_counter += 1
        processed.add(va)
    return twins_counter


def set_twin_nodes_constraints(solver: Parameters):
    twins_counter = 0
    twins_counter += __add_twins(solver.b, solver)
    twins_counter += __add_twins(solver.s, solver)
    return twins_counter
