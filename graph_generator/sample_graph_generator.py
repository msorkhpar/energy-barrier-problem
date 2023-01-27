import random


def __get_me_a_random_range(max_allowed_nodes):
    start = random.randint(1, max_allowed_nodes)
    end = random.randint(1, max_allowed_nodes)
    while start == end:
        start = random.randint(1, max_allowed_nodes)
        end = random.randint(1, max_allowed_nodes)
    if start > end:
        start, end = end, start
    return start, end


def __has_intersect(a1, a2, b1, b2):
    return (b1 < a1 < b2 < a2) or (a1 < b1 < a2 < b2) or (b1 == a1 or b2 == a2 or b2 == a1 or b1 == a2)


def generate_graph(max_allowed_nodes, max_allowed_pairs, trail=0):
    if trail > 10:
        return []
    result = []

    iter_no = 0
    while len(result) < max_allowed_pairs:
        start, end = __get_me_a_random_range(max_allowed_nodes)
        iter_no += 1
        if iter_no > 5000:
            print("Random graph generation failed, retrying from scratch...")
            return generate_graph(max_allowed_nodes, max_allowed_pairs)
        valid = True
        for left, right in result:
            if __has_intersect(left, right, start, end):
                valid = False
                break
        if valid:
            result.append((start, end))
    return result
