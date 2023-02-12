from networkx import Graph
from lp.solution import Solution
from persistent.models.BaseModel import BaseModel

from persistent.models.SampleGraph import SampleGraph
from persistent.models.BipartiteGraph import BipartiteGraph
from persistent.models.FractionalResult import FractionalResult
from persistent.models.IntegerResult import IntegerResult
import utility.json_utils as mapper

with BaseModel.get_db() as db:
    BaseModel.create_tables()


def __persist_graph(number_of_nodes, edges):
    with BaseModel.get_db() as db:
        g = SampleGraph(number_of_nodes=number_of_nodes, number_of_edges=len(edges), edges=edges)
        g.save()
        return g.graph_id


def __persist_bigraph(b_db_id, s_db_id, meta_info, b_len, s_len, number_of_edges, edges, node_mapping, prices):
    with BaseModel.get_db() as db:
        g = BipartiteGraph(
            b_graph=b_db_id,
            s_graph=s_db_id,
            meta_info=meta_info,
            b=b_len,
            s=s_len,
            number_of_edges=number_of_edges,
            edges=edges,
            node_mapping=node_mapping,
            prices=prices
        )
        g.save()
        return g.bigraph_id


def __update_lp_values(b_db_id, number_of_covered_neighborhood, number_of_twins, lp_variables_no, lp_constraints_no):
    with BaseModel.get_db() as db:
        bigraph = BipartiteGraph.get(BipartiteGraph.bigraph_id == b_db_id)
        bigraph.number_of_covered_neighborhood = number_of_covered_neighborhood
        bigraph.number_of_twins = number_of_twins
        bigraph.lp_variables_no = lp_variables_no
        bigraph.lp_constraints_no = lp_constraints_no
        bigraph.save()


def __update_integer_solution(b_db_id, integer_k, integer_solution_time):
    with BaseModel.get_db() as db:
        bigraph = BipartiteGraph.get(BipartiteGraph.bigraph_id == b_db_id)
        bigraph.integer_k = integer_k
        bigraph.integer_solution_time = integer_solution_time
        bigraph.save()


def __update_fractional_solution(b_db_id, fractional_k, fractional_solution_time):
    with BaseModel.get_db() as db:
        bigraph = BipartiteGraph.get(BipartiteGraph.bigraph_id == b_db_id)
        bigraph.fractional_k = fractional_k
        bigraph.fractional_solution_time = fractional_solution_time
        bigraph.save()


def __persist_integer_result(bigraph_db_id, k, values, sequence):
    with BaseModel.get_db() as db:
        result = IntegerResult(
            bipartite_graph=bigraph_db_id,
            k=k,
            values=values,
            sequence=sequence
        )
        result.save()
        return result.result_id


def __persist_fractional_result(bigraph_db_id, k, values):
    with BaseModel.get_db() as db:
        result = FractionalResult(
            bipartite_graph=bigraph_db_id,
            k=k,
            values=values,
        )
        result.save()
        return result.result_id


def persist_graphs(no_nodes, b, s):
    b_edges = [mapper.edge_mapper(from_node, to_node) for from_node, to_node in b]
    b_db_id = __persist_graph(no_nodes, b_edges)

    s_edges = [mapper.edge_mapper(from_node, to_node) for from_node, to_node in s]
    s_db_id = __persist_graph(no_nodes, s_edges)

    return b_db_id, s_db_id


def persist_bigraph(b_db_id: int, s_db_id: int, meta_info: str, b_len: int, s_len: int,
                    prices: dict, edge_mapper: dict, g: Graph):
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

    edges_list = [mapper.edge_mapper(from_node, to_nodes) for from_node, to_nodes in sorted(edges.items())]
    node_mapping = [mapper.edge_mapper(from_node, to_node) for from_node, to_node in edge_mapper.items()]

    return __persist_bigraph(b_db_id, s_db_id, meta_info, b_len, s_len, len(g.edges), edges_list, node_mapping, prices)


def persist_solution(bigraph_db_id: int, solution: Solution, l_len: int, fractional: bool):
    vals = [mapper.result_mapper(l_len, from_node, to_node) for from_node, to_node in solution.values.items()]
    if fractional:
        __update_fractional_solution(bigraph_db_id, solution.k, solution.solution_time)
        return __persist_fractional_result(bigraph_db_id, solution.k, vals)
    else:
        __update_integer_solution(bigraph_db_id, solution.k, solution.solution_time)
        return __persist_integer_result(bigraph_db_id, solution.k, vals, solution.sequence)


def persist_meta_data(b_db_id: int, solution: Solution):
    __update_lp_values(
        b_db_id, solution.number_of_covered_neighborhood, solution.number_of_twins,
        solution.variables_no, solution.constraints_no
    )
