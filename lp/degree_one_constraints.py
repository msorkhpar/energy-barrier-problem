from lp.utils import to_index, from_index

# processed_b = set()
# processed_s = set()
# for vb in b:
#     for vs in g[vb]:
#         if g.degree(vs) != 1:
#             continue
#         vars_dict.update({to_index(l_len, vb, vs): (1, 1)})
#         vars_dict.update({to_index(l_len, vs, vb): (0, 0)})
#         if vb not in processed_b:
#             for other_v in l:
#                 if other_v != vb and other_v not in processed_b and other_v not in processed_s:
#                     vars_dict.update({to_index(l_len, vb, other_v): (1, 1)})
#                     vars_dict.update({to_index(l_len, other_v, vb): (0, 0)})
#             processed_b.add(vb)
#
#         for other_v in l:
#             if other_v != vs and other_v not in processed_b and other_v not in processed_s:
#                 vars_dict.update({to_index(l_len, vs, other_v): (1, 1)})
#                 vars_dict.update({to_index(l_len, other_v, vs): (0, 0)})
#         processed_s.add(vs)

def add_degree_one_constraints(solver, variables, g, b, s, l):
    l_len = len(l)
    processed_b = set()
    processed_s = set()
    for vb in b:
        for vs in g[vb]:
            if g.degree(vs) != 1:
                continue
            if vb not in processed_b:
                for index in l:
                    if index not in processed_b and index not in processed_s and index != vb:
                        solver.Add(variables[to_index(l_len, vb, index)] == 1)
                processed_b.add(vb)

            for index in l:
                if index not in processed_b and index not in processed_s and index != vs:
                    solver.Add(variables[to_index(l_len, vb, index)] == 1)
            processed_s.add(vs)
