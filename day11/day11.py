from collections import Counter
from functools import lru_cache
from typing import Iterable


with open("day11/input.txt") as f:
    input = f.read().split()


def part_1() -> int:
    return _simulate(25)


def part_2() -> int:
    return _simulate(75)


@lru_cache
def _map_stones(stone_num: int) -> Iterable[int]:
    middle, rem = divmod(len(str(stone_num)), 2)
    if stone_num == 0:
        yield 1
    elif rem == 1:
        yield 2024 * stone_num
    else:
        yield divmod(stone_num, 10**middle)


def _simulate(iterations: int) -> int:
    stones = Counter(map(int, input))
    for _ in range(0, iterations):
        new_stones = Counter()
        for stone_id, stone_cnt in stones.items():
            for new_stone_id in _map_stones(stone_id):
                new_stones[new_stone_id] += stone_cnt
        stones = new_stones
    return sum(stones.values())
