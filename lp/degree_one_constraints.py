from lp.utils import to_index, from_index


def add_degree_one_constraints(solver, variables, g, b, l):
    processed_b = set()
    processed_s = set()
    for vb in b:
        for vs in g[vb]:
            if g.degree(vs) != 1:
                continue
            if vb not in processed_b:
                for index in l:
                    if index not in processed_b and index not in processed_s and index != vb:
                        solver.Add(variables[to_index(vb, index)] == 1)
                processed_b.add(vb)

            for index in l:
                if index not in processed_b and index not in processed_s and index != vs:
                    solver.Add(variables[to_index(vb, index)] == 1)
            processed_s.add(vs)
