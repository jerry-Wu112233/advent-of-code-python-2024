import re
from scipy import optimize

configs = []
with open("day13/input.txt", "r") as f:
    blocks = f.read().split("\n\n")
    for block in blocks:
        config = []
        for line in block.split("\n"):
            match = re.findall(r"(\d+)", line)
            config.append(list(map(int, match)))
        configs.append(config)

OBJ_FUNC_COEF = [3, 1]


def part_1() -> int:
    return sum(_optimize(config) for config in configs)


def part_2() -> int:
    return sum(_optimize(config, 10000000000000) for config in configs)


def _optimize(config: list[list[int]], b_eq_to_add: int = 0) -> int:
    A_eq_coefficients = [[config[0][0], config[1][0]], [config[0][1], config[1][1]]]
    b_eq_coefficients = [b_eq_to_add + coeff for coeff in config[2]]
    optimization_res = optimize.linprog(
        c=OBJ_FUNC_COEF, A_eq=A_eq_coefficients, b_eq=b_eq_coefficients
    )

    if optimization_res.success and _is_effectively_integer(optimization_res.fun):
        return round(optimization_res.fun)
    return 0


def _is_effectively_integer(num, tol=1e-3):
    return abs(num - round(num)) < tol
