from functools import lru_cache
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
    result = 0
    for seq in inputs:
        num_part = int(seq[:-1])
        key_pad_directions = _find_actions_for_keypad_seq(seq)

        first_directional_pad_seqs = []
        for key_pad_direction in key_pad_directions:
            first_directional_pad_seqs.extend(
                _find_actions_for_directional_seq(key_pad_direction)
            )

        min_direction_length = min(
            len(dir)
            for directional_seq in first_directional_pad_seqs
            for dir in _find_actions_for_directional_seq(directional_seq)
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


@lru_cache
def _find_actions_for_directional_seq(directional_seq: str) -> str:
    return _find_actions(directional_pad, directional_seq, directional_map)


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
            for coord_1, coord_2 in zip(path, path[1:]):
                for direction in _map_nodes_to_direction(coord_1, coord_2):
                    directions += direction
            directions += "A"
            for existing_path in actions:
                new_actions.append(existing_path + directions)
        actions = new_actions
        current_pos = next_pos
    return actions


actions = _find_actions(directional_pad, "<A^A>^^AvvvA", directional_map)
diff_count = set()
print(f"number of actions: {len(actions)}")
for i, action in enumerate(actions):
    next_level = _find_actions_for_directional_seq(action)
    for _, level in enumerate(next_level):
        diff_count.add((i, len(level)))

print(diff_count)
