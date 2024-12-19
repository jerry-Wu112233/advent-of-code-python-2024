from functools import lru_cache

patterns = set()
matchings = []
max_pattern_length = 0
with open("day19/input.txt", "r") as f:
    pattern_input, matching_input = f.read().split("\n\n")
    patterns = set(p.replace(" ", "") for p in pattern_input.split(","))
    matchings = [m for m in matching_input.split("\n")]
    for p in patterns:
        max_pattern_length = max(max_pattern_length, len(p))


def part_1() -> int:
    return sum(1 if _find_matching(match, 0) > 0 else 0 for match in matchings)


def part_2() -> int:
    return sum(_find_matching(match, 0) for match in matchings)


@lru_cache
def _find_matching(matching: str, index: int) -> int:
    if index == len(matching):
        return 1
    count = 0
    for i in range(0, max_pattern_length):
        if index + i >= len(matching):
            continue
        if matching[index : index + i + 1] in patterns:
            count += _find_matching(matching, index + i + 1)
    return count
