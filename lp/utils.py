from datetime import datetime


def to_index(l_len, i, j):
    return i * l_len + j


def from_index(l_len, index):
    index = int(index)
    if index == l_len ** 2:
        return "K", ""
    return index // l_len, index % l_len


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
