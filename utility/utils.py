from datetime import datetime


def set_l_len(__l_len):
    global l_len
    l_len = __l_len


def to_index(i, j):
    return i * l_len + j


def from_index(index):
    index = int(index)
    if index == l_len ** 2:
        return "K", ""
    return index // l_len, index % l_len


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
