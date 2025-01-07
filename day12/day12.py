from itertools import product

board = {}
with open("day12/input.txt") as f:
    for row, line in enumerate(f):
        for col, val in enumerate(line.rstrip("\n")):
            board |= {row + 1j * col: val}

directions = [-1, 1j, 1, -1j]
oct_dir = product([-1, 1], [-1, 1])
diagonal_dirs = {complex(a, b) for a, b in oct_dir}
diagonal_dirs_to_adj_dirs = {dir: (dir.real, 1j * dir.imag) for dir in diagonal_dirs}


def part_1() -> int:
    visited = set()
    aggregated_sum = 0
    for coord in board.keys():
        if coord in visited:
            continue
        visited.add(coord)
        perimeter, area = _find_perimeter_and_area(coord, visited)
        aggregated_sum += perimeter * area
    return aggregated_sum


def part_2() -> int:
    visited = set()
    aggregated_sum = 0
    for coord in board.keys():
        if coord in visited:
            continue
        num_of_sides, area = _find_number_of_edges_and_area(coord, visited)
        aggregated_sum += num_of_sides * area
    return aggregated_sum


def _find_number_of_edges_and_area(curr_pos: complex, visited: set) -> tuple[int, int]:
    character_to_find = board[curr_pos]
    corners = 0
    area = 0
    to_visit = [curr_pos]
    while to_visit:
        pos = to_visit.pop()
        if pos in visited:
            continue
        visited.add(pos)
        area += 1
        for diag_dir in diagonal_dirs:
            pos_to_check = pos + diag_dir
            adjacent_dir_1, adjacent_dir_2 = diagonal_dirs_to_adj_dirs[diag_dir]
            adjacent_pos_1 = pos + adjacent_dir_1
            adjacent_pos_2 = pos + adjacent_dir_2
            if (
                pos_to_check not in board.keys()
                or board[pos_to_check] != character_to_find
            ):
                if (
                    adjacent_pos_1 not in board.keys()
                    and adjacent_pos_2 not in board.keys()
                ):
                    corners += 1
                elif (
                    adjacent_pos_1 not in board.keys()
                    and board[adjacent_pos_2] != character_to_find
                    or adjacent_pos_2 not in board.keys()
                    and board[adjacent_pos_1] != character_to_find
                ):
                    corners += 1
                elif adjacent_pos_1 in board.keys() and adjacent_pos_2 in board.keys():
                    if (
                        board[adjacent_pos_1] == character_to_find
                        and board[adjacent_pos_2] == character_to_find
                    ):
                        corners += 1
                    elif (
                        board[adjacent_pos_1] != character_to_find
                        and board[adjacent_pos_2] != character_to_find
                    ):
                        corners += 1
            elif (
                board[pos_to_check] == character_to_find
                and board[adjacent_pos_1] != character_to_find
                and board[adjacent_pos_2] != character_to_find
            ):
                corners += 1

        for dir in directions:
            neighbor = pos + dir
            if neighbor in board.keys() and board[neighbor] == character_to_find:
                to_visit.append(neighbor)

    return corners, area


def _find_perimeter_and_area(curr_pos: complex, visited: set) -> tuple[int, int]:
    character_to_find = board[curr_pos]
    perimeter = 0
    area = 0
    to_visit = [curr_pos]
    while to_visit:
        pos = to_visit.pop()
        area += 1
        perimeter += 4
        for dir in directions:
            neighbor = pos + dir
            if neighbor in board.keys() and board[neighbor] == character_to_find:
                perimeter -= 1
                if neighbor not in visited:
                    to_visit.append(neighbor)
                    visited.add(neighbor)
    return perimeter, area


