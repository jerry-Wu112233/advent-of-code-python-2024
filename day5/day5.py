import networkx as nx

ordering = []
edges = []
with open("day5/input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if "|" in line:
            arr = line.split("|")
            edges.append((int(arr[0]), int(arr[1])))
        elif len(line) > 0:
            ordering.append([int(n) for n in line.split(",")])


def part_1() -> int:
    middle_page_sum = 0
    for order in ordering:
        filtered_topological_sort = _create_filtered_top_sort(order)
        if filtered_topological_sort == order:
            middle_page_sum += order[(len(order) - 1) // 2]
    return middle_page_sum


def part_2() -> int:
    middle_page_sum = 0
    for order in ordering:
        filtered_topological_sort = _create_filtered_top_sort(order)
        if filtered_topological_sort != order:
            middle_page_sum += filtered_topological_sort[(len(order) - 1) // 2]
    return middle_page_sum


def _create_filtered_top_sort(order: list[int]):
    # creates a topological sort for the provided nodes that respect the edge rules
    order_set = set(order)
    G = _make_graph_with_some_nodes(order)
    topological_sort = list(nx.topological_sort(G))
    return [node for node in topological_sort if node in order_set]


def _make_graph_with_some_nodes(node_set: set[int]):
    G = nx.DiGraph()
    for edge in edges:
        v1, v2 = edge
        if v1 in node_set and v2 in node_set:
            G.add_edge(v1, v2)
    return G
