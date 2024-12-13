with open("day10/input.txt") as f:
    ls = f.read().strip().split("\n")

board = {
    row + 1j * col: int(val)
    for row, line in enumerate(ls)
    for col, val in enumerate(line)
}


def part_1() -> int:
    return sum(len(set(_explore(coord))) for coord in board.keys() if board[coord] == 0)


def part_2() -> int:
    return sum(len(_explore(coord)) for coord in board.keys() if board[coord] == 0)


def _explore(current_pos: complex) -> list[complex]:
    directions = [1 + 0j, -1 + 0j, 0 + -1j, 0 + 1j]
    to_visit = [current_pos]
    zeniths = []
    while to_visit:
        position = to_visit.pop()
        if board[position] == 9:
            zeniths.append(position)
            continue
        for dir in directions:
            new_coord = position + dir
            if new_coord not in board.keys():
                continue
            if board[new_coord] != board[position] + 1:
                continue
            to_visit.append(new_coord)
    return zeniths
