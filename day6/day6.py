from concurrent.futures import ProcessPoolExecutor
from numbers import Number

initial_pos = (0, 0)
grid_x_dimension = 0
grid_y_dimension = 0
stops = set()

OUT_OF_BOUND_TUPLE = (-1, -1, 0, 0)

with open("day6/input.txt", "r") as f:
    for i, line in enumerate(f):
        grid_x_dimension += 1
        line = line.strip()
        for j, c in enumerate(line):
            grid_y_dimension = len(line)
            if c == "^":
                initial_pos = (i, j)
            elif c == "#":
                stops.add((i, j))


def part_1() -> int:
    return _simulate_walk()


def part_2() -> int:
    obstructions_that_cause_cycle = 0
    with ProcessPoolExecutor() as executor:
        extra_stops = [
            (i, j)
            for i in range(grid_x_dimension)
            for j in range(grid_y_dimension)
            if (i, j) not in stops and (i, j) != initial_pos
        ]
        results = executor.map(_simulate_walk, extra_stops)
        for path_length in results:
            obstructions_that_cause_cycle += 1 if path_length == 0 else 0
    return obstructions_that_cause_cycle


def _simulate_walk(extra_stop: tuple[int, int] = (-1, -1)) -> Number.Number:
    pos_and_direction = (initial_pos[0], initial_pos[1], -1, 0)
    visited_path = set()
    visited_coords_and_dir = set()
    while pos_and_direction != OUT_OF_BOUND_TUPLE:
        visited_path.add((pos_and_direction[0], pos_and_direction[1]))
        if pos_and_direction in visited_coords_and_dir:
            return float("inf")
        visited_coords_and_dir.add(pos_and_direction)
        pos_and_direction = _look_ahead(pos_and_direction, extra_stop)

    return len(visited_path)


def _look_ahead(
    pos_and_direction: tuple[int, int, int, int], extra_stop: tuple[int, int]
) -> tuple[int, int, int, int]:
    # returns a tuple containing next coordinate to walk to along with
    # tuple describing next direction
    curr_i, curr_j, x_direction, y_direction = pos_and_direction
    next_x = curr_i + x_direction
    next_y = curr_j + y_direction
    if _out_of_bound(next_x, next_y):
        return OUT_OF_BOUND_TUPLE

    if (next_x, next_y) not in stops and (next_x, next_y) != extra_stop:
        return (next_x, next_y, x_direction, y_direction)

    new_direction = (
        y_direction,
        -x_direction,
    )  # rotates the direction by pi / 2 radians clockwise

    return (curr_i, curr_j) + new_direction


def _out_of_bound(i: int, j: int) -> bool:
    return not (0 <= i < grid_x_dimension and 0 <= j < grid_y_dimension)


print(part_2())
