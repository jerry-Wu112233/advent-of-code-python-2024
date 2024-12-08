from typing import Iterator
import numpy as np
from collections import defaultdict
from itertools import chain, combinations


char_map = defaultdict(list)
grid_row_limit = 0
grid_col_limit = 0

with open("day8/input.txt") as f:
    lines = f.readlines()
    for row, line in enumerate(lines):
        grid_row_limit += 1
        line = line.rstrip("\n")
        for col, c in enumerate(line):
            grid_col_limit = len(line)
            if c == ".":
                continue
            char_map[c].append((row, col))


def part_1() -> int:
    return len(
        set(
            coord
            for c in char_map
            for coord_1, coord_2 in combinations(char_map[c], 2)
            for coord in _find_antinodes(coord_1, coord_2, 1)
        )
    )


def part_2() -> int:
    return len(
        set(
            coord
            for c in char_map
            for coord_1, coord_2 in combinations(char_map[c], 2)
            for coord in [coord_1, coord_2]
            + [node for node in _find_antinodes(coord_1, coord_2, float("inf"))]
        )
    )


def _find_antinodes(
    coordinate_1: tuple[int, int], coordinate_2: tuple[int, int], extensions: np.number
) -> Iterator[tuple[int, int]]:
    top_left_most_coord = coordinate_1 if coordinate_1 < coordinate_2 else coordinate_2
    bot_right_most_coord = (
        coordinate_1 if top_left_most_coord == coordinate_2 else coordinate_2
    )
    dx, dy = (
        bot_right_most_coord[0] - top_left_most_coord[0],
        bot_right_most_coord[1] - top_left_most_coord[1],
    )

    return chain(
        _generate_next_point(top_left_most_coord, (-dx, -dy), extensions),
        _generate_next_point(bot_right_most_coord, (dx, dy), extensions),
    )


def _generate_next_point(
    curr_coord: tuple[int, int], direction: tuple[int, int], iterations: np.number
) -> Iterator[tuple[int, int]]:
    t = 1
    while t <= iterations:
        next_x = curr_coord[0] + t * direction[0]
        next_y = curr_coord[1] + t * direction[1]
        if not _in_bound((next_x, next_y)):
            break
        yield (next_x, next_y)
        t += 1


def _in_bound(coordinate: tuple[int, int]) -> bool:
    return 0 <= coordinate[0] < grid_row_limit and 0 <= coordinate[1] < grid_col_limit
