from persistent.BaseModel import BaseModel

from persistent.SampleGraph import SampleGraph
from persistent.BipartiteGraph import BipartiteGraph
from persistent.FractionalResult import FractionalResult
from persistent.IntegerResult import IntegerResult
import persistent.utils as utils


def __get_bgraph(bgraph_db_id):
    with BaseModel.get_db() as db:
        return BipartiteGraph.get(BipartiteGraph.bgraph_id == bgraph_db_id)


def __get_fractional_result(bgraph_db_id):
    with BaseModel.get_db() as db:
        return FractionalResult.get(FractionalResult.bipartite_graph == bgraph_db_id)


def __get_integer_result(bgraph_db_id):
    with BaseModel.get_db() as db:
        return IntegerResult.get(IntegerResult.bipartite_graph == bgraph_db_id)


def __get_sample_graph(graph_db_id):
    with BaseModel.get_db() as db:
        return SampleGraph.get(SampleGraph.graph_id == graph_db_id)


def retrieve_integer_result(sample_db_id):
    with BaseModel.get_db() as db:
        sample_graph = __get_sample_graph(sample_db_id)


def retrieve_sample_graph(sample_db_id):
    with BaseModel.get_db() as db:
        sample_graph = __get_sample_graph(sample_db_id)


def retrieve_bgraph(bgraph_db_id):
    bgraph = __get_bgraph(bgraph_db_id)
    edges = []
    node_mapping = []
    b = set()
    s = set()
    for edge_data in bgraph.edges:
        from_node = edge_data['from']
        if from_node >= bgraph.b:
            s.add(from_node)
            break
        b.add(from_node)
        to_nodes = edge_data['to']
        for to_node in to_nodes:
            s.add(to_node)
            edges.append((from_node, to_node))

    for mapping in bgraph.node_mapping:
        node_mapping.append((mapping['to'], mapping['from']))

    integer_result = __get_integer_result(bgraph_db_id)
    return {
        "edges": edges, "node_mapping": node_mapping,
        "b": b, "s": s,
        "fractional_k": bgraph.fractional_k, "integer_k": bgraph.integer_k,
        "sequence": integer_result.sequence
    }


def retrieve_sample(bgraph_db_id):
    return retrieve_bgraph(bgraph_db_id)
