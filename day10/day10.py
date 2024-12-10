from collections import deque

board = dict()


with open("day10/input.txt", "r") as f:
    for row, line in enumerate(f):
        for col, val in enumerate(line.rstrip("\n")):
            try:
                board |= {row + 1j * col: int(val)}
            except ValueError as ve:
                board |= {row + 1j * col: float("inf")}


def part_1() -> int:
    return sum(len(set(_explore(coord))) for coord in board.keys() if board[coord] == 0)


def part_2() -> int:
    return sum(len(_explore(coord)) for coord in board.keys() if board[coord] == 0)


def _explore(current_pos: complex) -> list[complex]:
    directions = [1 + 0j, -1 + 0j, 0 + -1j, 0 + 1j]
    queue = deque()
    queue.append(current_pos)
    zeniths = []
    while queue:
        position = queue.popleft()
        if board[position] == 9:
            zeniths.append(position)
            continue
        for dir in directions:
            new_coord = position + dir
            if new_coord not in board.keys():
                continue
            if board[new_coord] != board[position] + 1:
                continue
            queue.append(new_coord)
    return zeniths
