#!/usr/bin/env python3
import os
import time
from lp.solver import solve
from persistent import db_service
from dotenv import load_dotenv
import pandas as pd

from graph_generator.bipartite_corrector import extract_nodes
from graph_generator.intersection_generator import create_bigraph_of_intersections
from graph_generator.bipartite_transformer import transform_bigraph
from graph_generator.sample_graph_generator import generate_graph
from graph_generator.random_bigraph_generator import generate_random_bigraph


def __print_seq(integer_solution, edge_mapper):
    print(f"sequence: [", end="")
    edge_mapper = {v: k for k, v in edge_mapper.items()}
    for seq in integer_solution['sequence']:
        print(f"{edge_mapper[seq]}, ", end="")
    print("]")


def __solve(g, b_len, s_len, fractional):
    start = time.time()
    result = solve(g, b_len, s_len, fractional)
    running_time = time.time() - start
    print(f"[ K is: '{result['k']}', with_fraction:'{fractional}' , running time in sec: '{running_time:.2f}' ]")
    result["solution_time"] = running_time
    return result


def run_random(b_size, s_size, min_no_edges, max_no_edges, meta_info):
    g, b, s = generate_random_bigraph(b_size, s_size, min_no_edges, max_no_edges)
    g, b, s = extract_nodes(g, b)
    return __run(g, meta_info)


def run_intersection(no_nodes, no_edges, meta_info):
    b = generate_graph(no_nodes, no_edges)
    s = generate_graph(no_nodes, no_edges)
    g, b, s = create_bigraph_of_intersections(b, s)
    g, b, s = extract_nodes(g, b)
    b_db_id, s_db_id = db_service.persist_graphs(no_nodes, b, s)
    return __run(g, meta_info, b_db_id, s_db_id)


def __run(g, meta_info, b_db_id=None, s_db_id=None):
    g, b, s, b_len, s_len, edge_mapper = transform_bigraph(g)
    bigraph_db_id = db_service.persist_bigraph(b_db_id, s_db_id, meta_info, b_len, s_len, edge_mapper, g)

    if b is not None:
        del b
    if s is not None:
        del s
    if edge_mapper is not None:
        del edge_mapper

    print(f"Final values before solving: |b|=[{b_len}], |s|=[{s_len}], |g|=[{len(g.edges())}]")
    integer_solution = __solve(g, b_len, s_len, False)
    db_service.persist_meta_data(bigraph_db_id, integer_solution)
    if integer_solution['k'] == -1:
        print(f"Solver could not find a solution for the given graph.")
        print(f"G nodes are [{g.nodes()}]")
        print(f"G edges are [{g.edges(data=False)}]")
        return

    db_service.persist_solution(bigraph_db_id, integer_solution, False)
    del integer_solution

    fractional_solution = __solve(g, b_len, s_len, True)
    db_service.persist_solution(bigraph_db_id, fractional_solution, True)
    del fractional_solution
    del g


if __name__ == '__main__':
    load_dotenv()

    generator_type = os.environ.get("GRAPH_GENERATOR_TYPE")
    if "RANDOM_BIGRAPH" == generator_type:
        df = pd.read_csv('plan-random.csv')
        for index, row in df.iterrows():
            b_size = row['b_size']
            s_size = row['s_size']
            min_no_edges = row['min_edges']
            max_no_edges = row['max_edges']
            no_samples = row['samples']
            meta_info = f"R_{index}"

            for i in range(no_samples):
                print("*" * 40)
                print(
                    f"Random Bigraph => round [{i + 1}/{no_samples}] with |b|=[{b_size}], |s|:[{s_size}],"
                    f" {min_no_edges}<=|g|<={max_no_edges} ({meta_info})")
                run_random(b_size, s_size, min_no_edges, max_no_edges, meta_info)

    elif "INTERSECTION" == generator_type:
        df = pd.read_csv('plan-intersection.csv')
        for index, row in df.iterrows():
            no_nodes = row['no_nodes']
            no_edges = row['no_edges']
            no_samples = row['samples']
            meta_info = f"I_{index}"

            for i in range(no_samples):
                print("*" * 40)
                print(
                    f"Intersection Graphs => round [{i + 1}/{no_samples}]  with |edges on each graph|=[{no_edges}] "
                    f"({meta_info})")
                run_intersection(no_nodes, no_edges, meta_info)

    else:
        print("Unknown graph generator type.")
        exit(1)
