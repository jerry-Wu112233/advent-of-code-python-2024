import re


def part_1(input_str: str) -> int:
    pattern = r"mul\((-?\d+\.?\d*),(-?\d+\.?\d*)\)"
    matches = re.findall(pattern, input_str)
    result = sum(int(n1) * int(n2) for n1, n2 in matches)
    return result


def part_2(input_str: str) -> int:
    pattern = r"do\(\)|don't\(\)|mul\(\d+,\d+\)"
    flag = True
    res = 0
    matches = re.findall(pattern, input_str)
    for match in matches:
        if match == "do()":
            flag = True
        elif match == "don't()":
            flag = False
        else:
            if not flag:
                continue
            res += part_1(match)
    return res
