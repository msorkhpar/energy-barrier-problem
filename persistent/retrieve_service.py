from persistent.models.BaseModel import BaseModel

from persistent.models.SampleGraph import SampleGraph
from persistent.models.BipartiteGraph import BipartiteGraph
from persistent.models.FractionalResult import FractionalResult
from persistent.models.IntegerResult import IntegerResult


def __get_bigraph(bigraph_db_id):
    with BaseModel.get_db() as db:
        return BipartiteGraph.get(BipartiteGraph.bigraph_id == bigraph_db_id)


def __get_fractional_result(bigraph_db_id):
    with BaseModel.get_db() as db:
        return FractionalResult.get(FractionalResult.bipartite_graph == bigraph_db_id)


def __get_integer_result(bigraph_db_id):
    with BaseModel.get_db() as db:
        return IntegerResult.get(IntegerResult.bipartite_graph == bigraph_db_id)


def __get_sample_graph(graph_db_id):
    with BaseModel.get_db() as db:
        return SampleGraph.get(SampleGraph.graph_id == graph_db_id)


def retrieve_integer_result(sample_db_id):
    with BaseModel.get_db() as db:
        sample_graph = __get_sample_graph(sample_db_id)


def retrieve_sample_graph(sample_db_id):
    with BaseModel.get_db() as db:
        sample_graph = __get_sample_graph(sample_db_id)


def retrieve_bigraph(bigraph_db_id):
    bigraph = __get_bigraph(bigraph_db_id)
    edges = []
    node_mapping = []
    b = set()
    s = set()
    for edge_data in bigraph.edges:
        from_node = edge_data['from']
        if from_node >= bigraph.b:
            s.add(from_node)
            break
        b.add(from_node)
        to_nodes = edge_data['to']
        for to_node in to_nodes:
            s.add(to_node)
            edges.append((from_node, to_node))

    for mapping in bigraph.node_mapping:
        node_mapping.append((mapping['to'], mapping['from']))

    integer_result = __get_integer_result(bigraph_db_id)
    return {
        "edges": edges, "node_mapping": node_mapping,
        "b": b, "s": s,
        "fractional_k": bigraph.fractional_k, "integer_k": bigraph.integer_k,
        "sequence": integer_result.sequence
    }


def retrieve_sample(bigraph_db_id):
    return retrieve_bigraph(bigraph_db_id)
