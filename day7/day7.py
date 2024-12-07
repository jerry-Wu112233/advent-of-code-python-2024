from itertools import product, starmap

left_hand_sides = []
right_hand_sides = []
with open("day7/input.txt", "r") as f:
    for line in f:
        inputs = line.split(":")
        left_hand_sides.append(int(inputs[0]))
        right_hand_sides.append([n for n in inputs[1].strip().split(" ")])


def part_1():
    return sum(
        left_hand_val
        for i, left_hand_val in enumerate(left_hand_sides)
        if left_hand_val in _generate_diff_eqns(right_hand_sides[i], 2)
    )


def part_2():
    return sum(
        left_hand_val
        for i, left_hand_val in enumerate(left_hand_sides)
        if left_hand_val in _generate_diff_eqns(right_hand_sides[i], 3)
    )


def _generate_diff_eqns(right_hand_side, operations):
    res = set()
    base_num_set = _generate_base_numbers_of_size_n(
        operations, len(right_hand_side) - 1
    )
    for c in base_num_set:
        c = starmap(_map_bin_str_to_operations, c)
        combined = [elem for pair in zip(right_hand_side, c) for elem in pair]
        combined.append(right_hand_side[-1])
        res.add(_left_to_right_eval(combined))
    return res


def _left_to_right_eval(tokens):
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


def _map_bin_str_to_operations(char_to_map):
    if char_to_map == "0":
        return "+"
    elif char_to_map == "1":
        return "*"
    return "|"


def _generate_base_numbers_of_size_n(base, n):
    # Generate all combinations of n digits in base 3
    return ["".join(map(str, digits)) for digits in product(range(base), repeat=n)]