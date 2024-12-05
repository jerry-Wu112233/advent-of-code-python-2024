import re
import networkx as nx
from collections import defaultdict, deque

with open("day5/input.txt", "r") as f:
    ls = f.read().strip().split("\n")


hierachy_pattern = r"(\d+)\|(\d+)"
predecessors = defaultdict(set)

ordering = []
edges = []
for line in ls:
    match = re.match(hierachy_pattern, line)
    if match:
        num1, num2 = match.groups()
        edges.append((int(num1), int(num2)))
    elif len(line) > 0:
        ordering.append([int(n) for n in line.split(",")])


def part_1() -> int:
    median_sum = 0
    for order in ordering:
        n = len(order)
        if _check_page_order(order):
            median_sum += order[(n - 1) // 2]
    return median_sum


def part_2() -> int:
    median_sum = 0
    for order in ordering:
        n = len(order)
        order_set = set(order)
        G = _make_graph_with_some_nodes(order)
        topological_sort = list(nx.topological_sort(G))
        filtered_topological_sort = [
            node for node in topological_sort if node in order_set
        ]

        if filtered_topological_sort != order:
            median_sum += filtered_topological_sort[(n - 1) // 2]
    return median_sum


def _check_page_order(order: list[int]) -> bool:
    G = _make_graph_with_some_nodes(order)
    topological_sort = list(nx.topological_sort(G))
    topological_sort_map = {
        topological_sort[i]: i for i in range(len(topological_sort))
    }
    n = len(order)
    return all(
        topological_sort_map[order[i]] > topological_sort_map[order[i - 1]]
        for i in range(1, n)
    )


def _make_graph_with_some_nodes(subset_of_nodes: list[int]):
    G = nx.DiGraph()
    node_set = set(subset_of_nodes)
    for edge in edges:
        v1, v2 = edge
        if v1 in node_set and v2 in node_set:
            G.add_edge(v1, v2)
    return G
