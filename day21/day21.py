from functools import lru_cache
from itertools import pairwise
import networkx as nx

with open("day21/input.txt", "r") as f:
    inputs = f.read().strip("\n").split("\n")

keypad_graph = nx.grid_2d_graph(4, 3)
keypad_graph.remove_node((3, 0))
keypad_map = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

directional_pad = nx.grid_2d_graph(2, 3)
directional_pad.remove_node((0, 0))
directional_map = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


def part_1() -> int:
    return _compute_cost_with_n_directional_layers(2)


def part_2() -> int:
    return _compute_cost_with_n_directional_layers(25)


def _compute_cost_with_n_directional_layers(directional_layers: int) -> int:
    result = 0
    for seq in inputs:
        num_part = int(seq[:-1])
        key_pad_directions = _find_actions_for_keypad_seq(seq)
        min_direction_length = float("inf")
        for direction in key_pad_directions:
            min_direction_length = min(
                min_direction_length, _find_num_of_paths(direction, directional_layers)
            )
        result += num_part * min_direction_length
    return result


def _map_nodes_to_direction(node_1: tuple[int, int], node_2: tuple[int, int]) -> str:
    r1, c1 = node_1
    r2, c2 = node_2
    if c2 == c1 + 1:
        return ">"
    elif c2 == c1 - 1:
        return "<"
    elif r2 == r1 + 1:
        return "v"
    elif r2 == r1 - 1:
        return "^"
    return ""


def _find_actions_for_keypad_seq(keypad_seq: str) -> str:
    return _find_actions(keypad_graph, keypad_seq, keypad_map)


def _find_actions(graph: nx.Graph, sequence: str, map_to_use: map) -> list[str]:
    current_pos = map_to_use["A"]
    actions = [""]
    for key in sequence:
        next_pos = map_to_use[key]

        paths = nx.all_shortest_paths(graph, source=current_pos, target=next_pos)
        new_actions = []
        for path in paths:
            directions = ""
            for coord_1, coord_2 in pairwise(path):
                for direction in _map_nodes_to_direction(coord_1, coord_2):
                    directions += direction
            directions += "A"
            for existing_path in actions:
                new_actions.append(existing_path + directions)
        actions = new_actions
        current_pos = next_pos
    return actions


@lru_cache
def _find_num_of_paths(path: str, robot_level: int) -> int:
    if robot_level == 0:
        return len(path)
    return sum(
        min(
            _find_num_of_paths(new_path + "A", robot_level - 1)
            for new_path in _get_all_paths(from_symbol, to_symbol)
        )
        for from_symbol, to_symbol in pairwise("A" + path)
    )


@lru_cache
def _get_all_paths(from_symbol: str, to_symbol: str, map_to_use: dict=directional_map) -> int:
    from_symbol_coord = map_to_use[from_symbol]
    to_symbol_coord = map_to_use[to_symbol]
    raw_paths = nx.all_shortest_paths(
        directional_pad, from_symbol_coord, to_symbol_coord
    )

    all_directions = []
    for path in raw_paths:
        directions = ""
        for coord_1, coord_2 in pairwise(path):
            for direction in _map_nodes_to_direction(coord_1, coord_2):
                directions += direction
        all_directions.append(directions)
    return all_directions
