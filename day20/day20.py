from itertools import combinations
from collections import deque

grid = {}

with open("day20/input.txt", "r") as f:
    for row, line in enumerate(f.read().split("\n")):
        for col, val in enumerate(line.strip()):
            m = len(line)
            coord = complex(row, col)

            if val == "S":
                start = coord
            if val != "#":
                grid |= {coord: val}

dist_map = {}
directions = (-1, 1, 1j, -1j)
visit_queue = deque([(start, 0)])

while visit_queue:
    curr_pos, dist_from_origin = visit_queue.popleft()
    if curr_pos in dist_map:
        continue
    if curr_pos not in grid.keys():
        continue
    dist_map[curr_pos] = dist_from_origin
    for dir in directions:
        visit_queue.append((curr_pos + dir, dist_from_origin + 1))


def part_1() -> int:
    counter = 0
    for (pos_1, dist_from_origin_1), (pos_2, dist_from_origin_2) in combinations(
        dist_map.items(), 2
    ):
        dist = abs(pos_1.real - pos_2.real) + abs(pos_1.imag - pos_2.imag)
        if dist == 2 and dist_from_origin_2 - dist_from_origin_1 - dist >= 100:
            counter += 1
    return counter


def part_2() -> int:
    counter = 0
    for (pos_1, dist_from_origin_1), (pos_2, dist_from_origin_2) in combinations(
        dist_map.items(), 2
    ):
        dist = abs(pos_1.real - pos_2.real) + abs(pos_1.imag - pos_2.imag)
        if dist < 21 and dist_from_origin_2 - dist_from_origin_1 - dist >= 100:
            counter += 1
    return counter
