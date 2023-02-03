import networkx as nx
import pandas as pd


def create_bgraph_of_intersections(g1_edges, g2_edges):
    g = nx.Graph()

    def get_index(graph_name, source, target):
        return f"{graph_name}({source},{target})"

    df = pd.DataFrame(g1_edges, columns=["source", "target"])
    intervals = pd.IntervalIndex.from_arrays(df.source, df.target, closed='both')
    edges = list()
    b = set()
    s = set()
    for source, target in g2_edges:
        overlaps = df[intervals.overlaps(pd.Interval(source - 0.1, target + 0.1))]
        overlaps = overlaps[((overlaps.source >= source) & (overlaps.target >= target)) | (
                (overlaps.source <= source) & (overlaps.target <= target))].to_numpy()
        s_index = get_index("S", source, target)
        for to in overlaps:
            b_index = get_index("B", to[0], to[1])
            b.add(b_index)
            s.add(s_index)
            edges.append((b_index, s_index))

    g.add_nodes_from([node for node in b], bipartite=0)
    g.add_nodes_from([node for node in s], bipartite=1)
    g.add_edges_from(edges)

    return g, b, s
