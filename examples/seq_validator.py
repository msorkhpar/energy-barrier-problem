import networkx as nx

from graph_generator.bipartite_corrector import extract_nodes
from graph_generator.bipartite_transformer import transform_bigraph
import utility.utils as utils


def run(edge_list, k: int, sequence):
    g, b, s = utils.create_bipartite_graph(edge_list)
    g, b, s = extract_nodes(g, b)
    g, b, s, b_len, s_len, edge_mapper = transform_bigraph(g)
    if len(sequence) != b_len + s_len:
        print("Invalid sequence!")
        print(f"Sequence length is not equal to the number of nodes in the graph!")
        return
    for turn in sequence:
        turn = turn.strip()
        if turn in b:
            k = k - 1
            g.remove_node(edge_mapper[turn])
        elif turn in s:
            if g.degree(edge_mapper[turn]) == 0:
                k = k + 1
                g.remove_node(edge_mapper[turn])
            else:
                print("Invalid sequence!")
                print(f"Attempting to remove a node with degree > 0 from S side => node:[{turn}]")
                return
        else:
            print("Invalid sequence!")
            print(f"Given edge[{turn}] is not a part of the graph!!")
            return
        if k < 0:
            print("Invalid sequence!")
            print(f"K become negative by removing [{turn}] Not a valid sequence")
            return
    print("Sequence is valid!")


if __name__ == '__main__':
    example_number = input("Which example do you want to run (enter the number only)?")
    k = int(input("Enter the K value"))
    sequence = input("Enter the sequence(comma separated)").split(",")
    sequence = list(map(str.strip, sequence))
    # B to S edge list
    with open(f'{example_number}.txt') as f:
        edge_list = [tuple(map(str.strip, i.split(','))) for i in f]
    run(edge_list, k, sequence)
