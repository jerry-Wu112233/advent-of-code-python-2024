import re

from itertools import starmap, product
from typing import Tuple


def part_1(file_path_to_input: str) -> int:
    xmas_count = 0
    grid = _get_grid(file_path_to_input)
    XMAS_STR = "XMAS"
    x_limit = len(grid)
    y_limit = len(grid[0])

    def get_char_from_coord(i: int, j: int) -> str:
        if not (0 <= i < x_limit and 0 <= j < y_limit):
            return ""
        return grid[i][j]

    for i in range(x_limit):
        for j in range(y_limit):
            if grid[i][j] != "X":
                continue
            search_coords, _ = _get_coords_in_all_dir(i, j, 4)
            for coordinates in search_coords:
                if len(coordinates) != len(XMAS_STR):
                    continue
                word = "".join(starmap(get_char_from_coord, coordinates))
                xmas_count += 1 if word == XMAS_STR else 0
    return xmas_count


def part_2(file_path_to_input: str) -> int:
    XMAS_ROW_1_PATTERN = r"M.S"
    XMAS_ROW_2_PATTERN = r".A."
    XMAS_ROW_3_PATTERN = r"M.S"

    patterns = [XMAS_ROW_1_PATTERN, XMAS_ROW_2_PATTERN, XMAS_ROW_3_PATTERN]
    grid = _get_grid(file_path_to_input)
    x_limit = len(grid)
    y_limit = len(grid[0])

    block_count = 0

    def construct_xmas_block(
        coordinate_list: list[list[Tuple[int, int]]],
        reference_block: list[list[Tuple[int, int]]],
    ) -> list[str]:
        default_block = [["o", "w", "o"], ["O", "w", "O"], ["o", "w", "o"]]
        for i in range(len(reference_block)):
            for j in range(len(reference_block[i])):
                transformed_x = reference_block[i][j][0]
                transformed_y = reference_block[i][j][1]
                actual_x = coordinate_list[i][j][0]
                actual_y = coordinate_list[i][j][1]
                if not (0 <= actual_x < x_limit and 0 <= actual_y < y_limit):
                    return default_block

                default_block[transformed_x][transformed_y] = grid[actual_x][actual_y]
        return default_block

    for i in range(x_limit):
        for j in range(y_limit):
            if grid[i][j] != "A":
                continue
            coord_list, reference_block = _get_coords_in_all_dir(i, j, 2)
            original_block = construct_xmas_block(coord_list, reference_block)
            for block in _all_rotations(original_block):
                block_count += (
                    1
                    if all(
                        bool(re.fullmatch(patterns[idx], "".join(block[idx])))
                        for idx in range(3)
                    )
                    else 0
                )

    return block_count


def _get_coords_in_all_dir(
    current_x: int, current_y: int, increment_total: int
) -> Tuple[list[list[Tuple[int, int]]], list[list[Tuple[int, int]]]]:
    directions = set(product((-1, 0, 1), (-1, 0, 1))) - {(0, 0)}
    search_results = []
    reference_block = []
    for x_dir, y_dir in directions:
        search_results.append(
            [
                (current_x + x_dir * increment, current_y + y_dir * increment)
                for increment in range(increment_total)
            ]
        )
        reference_block.append(
            [
                (1 + x_dir * increment, 1 + y_dir * increment)
                for increment in range(increment_total)
            ]
        )
    return search_results, reference_block


def _get_grid(file_path_to_input: str) -> list[list[str]]:
    grid = []
    with open(file_path_to_input, "r") as f:
        for line in f:
            grid.append([c for c in line if c != "\n"])
    return grid


def _rotate_90(arr: list[list[str]]):
    return [list(row) for row in zip(*arr[::-1])]


def _all_rotations(arr: list[list[list[str]]]):
    rotations = []
    current = arr
    for _ in range(4):
        current = _rotate_90(current)
        rotations.append(current)
    return rotations