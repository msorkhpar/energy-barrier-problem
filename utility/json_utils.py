from utility.utils import from_index


def edge_mapper(from_node="", to_node=""):
    return {"from": from_node, "to": to_node}


def result_mapper(l_len, index, value):
    i_index, j_index = from_index(l_len, index)
    return {"index": index, "index_name": f"X({i_index},{j_index})", "value": value}
