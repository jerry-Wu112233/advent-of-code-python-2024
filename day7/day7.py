from itertools import product, starmap, filterfalse
from typing import Iterator

left_hand_sides = []
right_hand_sides = []
with open("day7/input.txt", "r") as f:
    for line in f:
        inputs = line.split(":")
        left_hand_sides.append(int(inputs[0]))
        right_hand_sides.append(inputs[1].strip().split(" "))


def part_1():
    # rewrite the below with itertools filterfalse
    return sum(
        left_hand_val
        for i, left_hand_val in enumerate(left_hand_sides)
        if left_hand_val
        in filterfalse(
            lambda x: _left_to_right_eval(x) == left_hand_val,
            _generate_diff_eqns(right_hand_sides[i], 2),
        )
    )
    # return sum(
    #     left_hand_val
    #     for i, left_hand_val in enumerate(left_hand_sides)
    #     if left_hand_val in _generate_diff_eqns(right_hand_sides[i], 2)
    # )


def part_2():
    return sum(
        left_hand_val
        for i, left_hand_val in enumerate(left_hand_sides)
        if left_hand_val in _generate_diff_eqns(right_hand_sides[i], 3)
    )


def _generate_diff_eqns(right_hand_side, operations) -> Iterator:
    base_num_set = _generate_base_numbers_of_size_n(
        operations, len(right_hand_side) - 1
    )
    for c in base_num_set:
        c = starmap(_map_bin_str_to_operations, c)
        combined = [elem for pair in zip(right_hand_side, c) for elem in pair]
        combined.append(right_hand_side[-1])
        yield combined


def _left_to_right_eval(tokens: list[str]) -> int:
    result = int(tokens[0])
    for i in range(1, len(tokens), 2):
        operator = tokens[i]
        operand = int(tokens[i + 1])
        if operator == "+":
            result += operand
        elif operator == "*":
            result *= operand
        else:
            result = int(str(result) + str(operand))
    return result


def _map_bin_str_to_operations(char_to_map: str) -> str:
    match char_to_map:
        case "0":
            return "+"
        case "1":
            return "*"
        case _:
            return "|"


def _generate_base_numbers_of_size_n(base: int, n: int) -> list[str]:
    return ["".join(map(str, digits)) for digits in product(range(base), repeat=n)]


for eqns in _generate_diff_eqns(right_hand_sides[0], 2):
    print(eqns)
