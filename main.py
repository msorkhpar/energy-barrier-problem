#!/usr/bin/env python3
import os
import time
import sys

import dotenv

from graph_generator.bgraph_corrector import omit_degree_ones_from_bgraph
from graph_generator.bipartite_generator import create_bgraph_of_intersections
from graph_generator.bipartite_transformer import transform_bgraph
from graph_generator.sample_graph_generator import generate_graph
from lp.solver import solve
from persistent import db_service
from dotenv import load_dotenv, find_dotenv


def __solve(g, b_len, s_len, fractional):
    start = time.time()
    result = solve(g, b_len, s_len, fractional,os.environ.get('NUMBER_OF_THREADS'))
    running_time = time.time() - start
    print("*" * 120)
    print(f"[ K is: '{result['k']}', with_fraction:'{fractional}' , running time in sec: '{running_time:.2f}' ]")
    result["running_time"] = running_time
    return result


def run(no_nodes, no_edges):
    b = sorted(generate_graph(no_nodes, no_edges))

    s = sorted(generate_graph(no_nodes, no_edges))

    g = create_bgraph_of_intersections(b, s)
    g, b, s = omit_degree_ones_from_bgraph(g)
    g, b_len, s_len, edge_mapper = transform_bgraph(g)

    b_db_id, s_db_id = db_service.persist_graphs(no_nodes, b, s)
    bgraph_db_id = db_service.persist_bgraph(b_db_id, s_db_id, b_len, s_len, edge_mapper, g)
    del b
    del s
    del edge_mapper
    l_len = s_len + b_len
    integer_solution = __solve(g, b_len, s_len, False)
    db_service.persist_meta_data(
        bgraph_db_id, integer_solution["number_of_covered_neighborhood"], integer_solution["variables_no"],
        integer_solution["constraints_no"]
    )
    db_service.persist_solution(
        bgraph_db_id, l_len, integer_solution['k'], integer_solution['values'],
        False, integer_solution['running_time'], integer_solution['sequence']
    )
    del integer_solution
    fractional_solution = __solve(g, b_len, s_len, True)
    db_service.persist_solution(
        bgraph_db_id, l_len, fractional_solution['k'], fractional_solution['values'],
        True, fractional_solution['running_time']
    )
    del fractional_solution


if __name__ == '__main__':
    load_dotenv()
    no_nodes = int(os.environ.get("NUMBER_OF_VERTICES"))
    no_samples = int(os.environ.get("NUMBER_OF_SAMPLES"))
    min_no_edges = int(os.environ.get("MIN_NUMBER_OF_EDGES"))
    max_no_edges = int(os.environ.get("MAX_NUMBER_OF_EDGES"))
    for no_edges in range(min_no_edges, max_no_edges + 1):
        for i in range(no_samples):
            print(f"round {i + 1} of {no_samples} for [{no_edges}] edges")
            run(no_nodes, no_edges)
