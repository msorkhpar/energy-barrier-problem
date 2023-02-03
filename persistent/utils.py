from lp.utils import from_index


def edge(from_node="", to_node=""):
    return {"from": from_node, "to": to_node}


def result(index, value):
    i_index, j_index = from_index(index)
    return {"index": index, "index_name": f"X({i_index},{j_index})", "value": value}
