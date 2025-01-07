import re
from typing import Optional

with open("day17/input.txt", "r") as f:
    register_initial_state, instructions_input = f.read().split("\n\n")
    matches = re.findall(r"(\w):\s*(\d+)", register_initial_state)
    registers = {key: int(value) for key, value in matches}
    instructions = list(map(int, instructions_input.split(":")[1].strip().split(",")))


def part_1():
    output = []
    pointer_index = 0
    while pointer_index < len(instructions):
        pointer_index, command_res = execute_command(pointer_index)
        if command_res is not None:
            output.append(command_res)
    return ",".join(map(str, output))


def execute_command(pointer_index: int) -> tuple[int, Optional[int]]:
    operand_1 = instructions[pointer_index]
    operand_2 = instructions[pointer_index + 1]
    match operand_1:
        case 0:
            registers["A"] = _div(operand_2)
        case 1:
            registers["B"] ^= operand_2
        case 2:
            registers["B"] = _get_combo_operand(operand_2) % 8
        case 3:
            if registers["A"] != 0:
                return (operand_2, None)
        case 4:
            registers["B"] = registers["B"] ^ registers["C"]
        case 5:
            return (pointer_index + 2, _get_combo_operand(operand_2) % 8)
        case 6:
            registers["B"] = _div(operand_2)
        case 7:
            registers["C"] = _div(operand_2)

    return (pointer_index + 2, None)


def _get_combo_operand(operand: int) -> int:
    match operand:
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case _:
            return operand


def _div(operand: int) -> int:
    return registers["A"] >> _get_combo_operand(operand)
