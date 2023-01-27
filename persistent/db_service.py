from persistent.BaseModel import BaseModel

from persistent.SampleGraph import SampleGraph
from persistent.BipartiteGraph import BipartiteGraph
from persistent.FractionalResult import FractionalResult
from persistent.IntegerResult import IntegerResult
import persistent.utils as utils

with BaseModel.get_db() as db:
    BaseModel.create_tables()


def __persist_graph(number_of_nodes, edges):
    with BaseModel.get_db() as db:
        g = SampleGraph(number_of_nodes=number_of_nodes, number_of_edges=len(edges), edges=edges)
        g.save()
        return g.graph_id


def __persist_bgraph(b_db_id, s_db_id, b_len, s_len, number_of_edges, edges, node_mapping):
    with BaseModel.get_db() as db:
        g = BipartiteGraph(
            b_graph=b_db_id,
            s_graph=s_db_id,
            b=b_len,
            s=s_len,
            number_of_edges=number_of_edges,
            edges=edges,
            node_mapping=node_mapping
        )
        g.save()
        return g.bgraph_id


def __update_lp_values(b_db_id, number_of_covered_neighborhood,number_of_twins, lp_variables_no, lp_constraints_no):
    with BaseModel.get_db() as db:
        bgraph = BipartiteGraph.get(BipartiteGraph.bgraph_id == b_db_id)
        bgraph.number_of_covered_neighborhood = number_of_covered_neighborhood
        bgraph.number_of_twins = number_of_twins
        bgraph.lp_variables_no = lp_variables_no
        bgraph.lp_constraints_no = lp_constraints_no
        bgraph.save()


def __update_integer_solution(b_db_id, integer_k, integer_solution_time):
    with BaseModel.get_db() as db:
        bgraph = BipartiteGraph.get(BipartiteGraph.bgraph_id == b_db_id)
        bgraph.integer_k = integer_k
        bgraph.integer_solution_time = integer_solution_time
        bgraph.save()


def __update_fractional_solution(b_db_id, fractional_k, fractional_solution_time):
    with BaseModel.get_db() as db:
        bgraph = BipartiteGraph.get(BipartiteGraph.bgraph_id == b_db_id)
        bgraph.fractional_k = fractional_k
        bgraph.fractional_solution_time = fractional_solution_time
        bgraph.save()


def __persist_integer_result(bgraph_db_id, k, values, sequence):
    with BaseModel.get_db() as db:
        result = IntegerResult(
            bipartite_graph=bgraph_db_id,
            k=k,
            values=values,
            sequence=sequence
        )
        result.save()
        return result.result_id


def __persist_fractional_result(bgraph_db_id, k, values):
    with BaseModel.get_db() as db:
        result = FractionalResult(
            bipartite_graph=bgraph_db_id,
            k=k,
            values=values)
        result.save()
        return result.result_id


def persist_graphs(no_nodes, b, s):
    b_edges = [utils.edge(from_node, to_node) for from_node, to_node in b]
    b_db_id = __persist_graph(no_nodes, b_edges)

    s_edges = [utils.edge(from_node, to_node) for from_node, to_node in s]
    s_db_id = __persist_graph(no_nodes, s_edges)

    return b_db_id, s_db_id


def persist_bgraph(b_db_id, s_db_id, b_len, s_len, edge_mapper, g):
    edges = dict()
    for from_node, to_node in g.edges:
        # from -> to
        nodes = edges.get(from_node, [])
        nodes.append(to_node)
        edges[from_node] = nodes
        # to -> from
        nodes = edges.get(to_node, [])
        nodes.append(from_node)
        edges[to_node] = nodes

    edges_list = [utils.edge(from_node, to_nodes) for from_node, to_nodes in sorted(edges.items())]
    node_mapping = [utils.edge(from_node, to_node) for from_node, to_node in edge_mapper.items()]

    return __persist_bgraph(b_db_id, s_db_id, b_len, s_len, len(g.edges), edges_list, node_mapping)


def persist_solution(bgraph_db_id, l_len, k, values, fractional, solution_time, sequence=None):
    vals = [utils.result(l_len, from_node, to_node) for from_node, to_node in values.items()]
    if fractional:
        __update_fractional_solution(bgraph_db_id, k, solution_time)
        return __persist_fractional_result(bgraph_db_id, k, vals)
    else:
        __update_integer_solution(bgraph_db_id, k, solution_time)
        return __persist_integer_result(bgraph_db_id, k, vals, sequence)


def persist_meta_data(b_db_id, number_of_covered_neighborhood,number_of_twins, lp_variables_no, lp_constraints_no):
    __update_lp_values(b_db_id, number_of_covered_neighborhood,number_of_twins, lp_variables_no, lp_constraints_no)
