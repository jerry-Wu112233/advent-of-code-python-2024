import networkx as nx
from itertools import product

grid = {}

start = None
end = None

with open("day16/input.txt", "r") as f:
    for row, line in enumerate(f):
        for col, val in enumerate(line.rstrip("\n")):
            coord = row + 1j * col
            if val == "#":
                continue
            grid |= {coord: val}
            if val == "S":
                start = coord
            elif val == "E":
                end = coord

directions = {1j, -1, -1j, 1}
G = nx.DiGraph()
G.add_nodes_from((pos, dir) for pos in grid.keys() for dir in directions)
for pos in grid.keys():
    for dir_1, dir_2 in product(directions, directions):
        if dir_1 == dir_2 and pos + dir_1 in grid.keys():
            G.add_edge((pos, dir_1), (pos + dir_1, dir_2), weight=1)
        elif dir_1 != -dir_2:
            G.add_edge((pos, dir_1), (pos, dir_2), weight=1000)


def part_1():
    return _min_cost_of_best_path()


def part_2():
    start_node = (start, 1j)
    min_cost = _min_cost_of_best_path()
    node_set = set()
    for dir in directions:
        try:
            curr_dist = nx.shortest_path_length(
                G, source=start_node, target=(end, dir), weight="weight"
            )
            if curr_dist != min_cost:
                continue
            paths = list(
                nx.all_shortest_paths(
                    G, source=start_node, target=(end, dir), weight="weight"
                )
            )

            for path in paths:
                for node, _ in path:
                    node_set.add(node)
        except nx.NetworkXNoPath:
            continue
    return len(node_set)


def _min_cost_of_best_path() -> int:
    start_node = (start, 1j)
    min_cost = float("inf")
    for dir in directions:
        try:
            min_cost = min(
                min_cost,
                nx.shortest_path_length(
                    G, source=start_node, target=(end, dir), weight="weight"
                ),
            )
        except nx.NetworkXNoPath:
            continue
    return min_cost
