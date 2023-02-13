#!/usr/bin/env python3

import os
import queue
import random
import time
from multiprocessing import Process, Queue

from lp.solver import Parameters, Solver
import persistent.db_service as db_service
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


def __solve(bigraph_db_id, g, b_len, s_len, price_dict, fractional):
    problem_type = 'Fractional' if fractional else 'Integer'
    print(f"Initializing {problem_type}-solver for Bigraph[{bigraph_db_id}]")
    start = time.time()
    parameters = Parameters(g, b_len, s_len, fractional, price_dict)
    result = Solver(parameters).solve()
    running_time = time.time() - start
    print(
        f"Bigraph[ {bigraph_db_id} ]=> {problem_type} K is: [ {result.k} ], "
        f"running time in sec: '{running_time:.2f}' ")
    result.set_solution_time(running_time)
    db_service.persist_meta_data(bigraph_db_id, result)

    if result.k == -1:
        print(f"Solver could not find a solution for the given graph.")
        print(f"G nodes are [{g.nodes()}]")
        print(f"G edges are [{g.edges(data=False)}]")
        del result
        return

    db_service.persist_solution(bigraph_db_id, result, parameters.l_len, fractional)
    del result


class RandomData:
    def __init__(self, round_no, no_samples, b_size, s_size, min_no_edges, max_no_edges, meta_info, with_prices):
        self.round_no = round_no
        self.no_samples = no_samples
        self.b_size = b_size
        self.s_size = s_size
        self.min_no_edges = min_no_edges
        self.max_no_edges = max_no_edges
        self.meta_info = meta_info
        self.with_prices = with_prices


def run_random(random_data: RandomData):
    print("*" * 40)
    print(f"Random Bigraph => round [{random_data.round_no + 1}/{random_data.no_samples}] with "
          f"|b|=[{random_data.b_size}], |s|:[{random_data.s_size}],"
          f" {random_data.min_no_edges}<=|g|<={random_data.max_no_edges} ({random_data.meta_info})")
    print("*" * 40)
    g, b, s = generate_random_bigraph(
        random_data.b_size, random_data.s_size, random_data.min_no_edges, random_data.max_no_edges
    )
    g, b, s = extract_nodes(g, b)
    bigraph_db_id = __run(g, random_data.meta_info, random_data.with_prices)
    print(f"Bigraph[ {bigraph_db_id} ] has been finished")
    return bigraph_db_id


class IntersectionData:
    def __init__(self, round_no, no_samples, no_nodes, no_edges, meta_info, with_prices):
        self.round_no = round_no
        self.no_samples = no_samples
        self.no_nodes = no_nodes
        self.no_edges = no_edges
        self.meta_info = meta_info
        self.with_prices = with_prices


def run_intersection(intersection_data: IntersectionData):
    print("*" * 40)
    print(f"Intersection Graphs => round [{intersection_data.round_no + 1}/{intersection_data.no_samples}]  with "
          f"|g|=[{intersection_data.no_edges}] ({intersection_data.meta_info})")
    print("*" * 40)

    b = generate_graph(intersection_data.no_nodes, intersection_data.no_edges)
    s = generate_graph(intersection_data.no_nodes, intersection_data.no_edges)
    g, b, s = create_bigraph_of_intersections(b, s)
    g, b, s = extract_nodes(g, b)
    b_db_id, s_db_id = db_service.persist_graphs(intersection_data.no_nodes, b, s)
    return __run(g, intersection_data.meta_info, intersection_data.with_prices, b_db_id, s_db_id)


def __generate_random_price_dict(b_len, s_len):
    l_len = b_len + s_len
    price_dict = {ele: random.randint(1, 100 * l_len) for ele in range(b_len)}
    price_dict.update({ele: random.randint(1, 100 * l_len) for ele in range(b_len, l_len)})

    return price_dict


def __run(g, meta_info, with_prices, b_db_id=None, s_db_id=None):
    g, b, s, b_len, s_len, edge_mapper = transform_bigraph(g)
    price_dict = None if not with_prices else __generate_random_price_dict(b_len, s_len)
    bigraph_db_id = db_service.persist_bigraph(b_db_id, s_db_id, meta_info, b_len, s_len, price_dict, edge_mapper, g)

    if b is not None:
        del b
    if s is not None:
        del s
    if edge_mapper is not None:
        del edge_mapper

    print(f"Final values before solving: |b|=[{b_len}], |s|=[{s_len}], |g|=[{len(g.edges())}]")
    __solve(bigraph_db_id, g, b_len, s_len, price_dict, True)
    # run integer solver in a separate process
    integer_process = Process(target=__solve, args=(bigraph_db_id, g, b_len, s_len, price_dict, False))
    integer_process.start()
    integer_process.join()

    del g
    return bigraph_db_id


# https://www.digitalocean.com/community/tutorials/python-multiprocessing-example
def do_job(tasks_to_accomplish: Queue):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
            if isinstance(task, RandomData):
                run_random(task)
            elif isinstance(task, IntersectionData):
                run_intersection(task)
        except queue.Empty:
            time.sleep(10)
            break


if __name__ == '__main__':
    load_dotenv()
    db_service.create_tables()
    number_of_processes = int(os.environ.get("NUMBER_OF_PROCESSES"))
    tasks_to_accomplish = Queue()
    processes = []

    generator_type = os.environ.get("GRAPH_GENERATOR_TYPE")
    with_prices = os.environ.get("WITH_PRICES") == "True"
    if "RANDOM_BIGRAPH" == generator_type:
        df = pd.read_csv('plan-random.csv')
        for index, row in df.iterrows():
            no_samples = row['samples']
            for i in range(no_samples):
                tasks_to_accomplish.put(
                    RandomData(i, no_samples, row['b_size'], row['s_size'], row['min_edges'], row['max_edges'],
                               f"R_{'P_' if with_prices else ''}{index}", with_prices)
                )

    elif "INTERSECTION" == generator_type:
        df = pd.read_csv('plan-intersection.csv')
        for index, row in df.iterrows():
            no_samples = row['samples']

            for i in range(no_samples):
                tasks_to_accomplish.put(
                    IntersectionData(i, no_samples, row['no_nodes'], row['no_edges'],
                                     f"I_{'P_' if with_prices else ''}{index}{index}", with_prices)
                )
    else:
        print("Unknown graph generator type.")
        exit(1)

    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
