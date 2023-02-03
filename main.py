#!/usr/bin/env python3
import os
import time

from graph_generator.bgraph_corrector import omit_degree_ones_from_bgraph
from graph_generator.bipartite_generator import create_bgraph_of_intersections
from graph_generator.bipartite_transformer import transform_bgraph
from graph_generator.sample_graph_generator import generate_graph
from random_graph_generator.random_graph_generator import generate_random_bigraph
from lp.solver import solve
from persistent import db_service
from dotenv import load_dotenv


def __print_seq(integer_solution, edge_mapper):
    print(f"sequence: [", end="")
    edge_mapper = {v: k for k, v in edge_mapper.items()}
    for seq in integer_solution['sequence']:
        print(f"{edge_mapper[seq]}, ", end="")
    print("]")


def __solve(g, b_len, s_len, fractional):
    start = time.time()
    result = solve(g, b_len, s_len, fractional, int(os.environ.get('NUMBER_OF_THREADS')))
    running_time = time.time() - start
    print(f"[ K is: '{result['k']}', with_fraction:'{fractional}' , running time in sec: '{running_time:.2f}' ]")
    result["running_time"] = running_time
    return result


def run(no_nodes, no_edges):
    b = s = b_db_id = s_db_id = None

    if "RANDOM_BIGRAPH" == os.environ.get("GRAPH_GENERATOR_TYPE"):
        g, b, s = generate_random_bigraph(
            no_edges,
            int(os.environ.get("BIGRAPH_MAX_EDGES")),
            int(os.environ.get("BIGRAPH_MIN_EDGES"))
        )

    elif "INTERSECTION" == os.environ.get("GRAPH_GENERATOR_TYPE"):
        b = generate_graph(no_nodes, no_edges)
        s = generate_graph(no_nodes, no_edges)
        g, b, s = create_bgraph_of_intersections(b, s)
    else:
        print("Unknown graph generator type.")
        exit(1)

    # g, b, s = omit_degree_ones_from_bgraph(g)

    if "INTERSECTION" == os.environ.get("GRAPH_GENERATOR_TYPE"):
        b_db_id, s_db_id = db_service.persist_graphs(no_nodes, b, s)

    g, b_len, s_len, edge_mapper = transform_bgraph(g)
    bgraph_db_id = db_service.persist_bgraph(b_db_id, s_db_id, b_len, s_len, edge_mapper, g)

    if b is not None:
        del b
    if s is not None:
        del s

    integer_solution = __solve(g, b_len, s_len, False)
    db_service.persist_meta_data(
        bgraph_db_id, integer_solution["number_of_covered_neighborhood"], integer_solution["number_of_twins"],
        integer_solution["variables_no"], integer_solution["constraints_no"]
    )
    if integer_solution['k'] == -1:
        print(f"Solver could not find a solution for the given graph.")
        print(f"G nodes are [{g.nodes()}]")
        print(f"G edges are [{g.edges(data=False)}]")
        return
    db_service.persist_solution(
        bgraph_db_id, integer_solution['k'], integer_solution['values'],
        False, integer_solution['running_time'], integer_solution['sequence']
    )
    #__print_seq(integer_solution, edge_mapper)
    del integer_solution
    fractional_solution = __solve(g, b_len, s_len, True)
    db_service.persist_solution(
        bgraph_db_id, fractional_solution['k'], fractional_solution['values'],
        True, fractional_solution['running_time']
    )
    del fractional_solution


if __name__ == '__main__':
    load_dotenv()
    no_vertices = int(os.environ.get("NUMBER_OF_VERTICES"))
    no_samples = int(os.environ.get("NUMBER_OF_SAMPLES"))
    min_no_edges = int(os.environ.get("MIN_NUMBER_OF_EDGES"))
    max_no_edges = int(os.environ.get("MAX_NUMBER_OF_EDGES"))
    for no_edges in range(min_no_edges, max_no_edges + 1):
        for i in range(no_samples):
            print("*" * 120)
            print(f"round {i + 1} of {no_samples} for [{no_edges}] edges")
            run(no_vertices, no_edges)
            print("*" * 120)
