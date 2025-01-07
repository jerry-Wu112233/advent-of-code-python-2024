grid = {}
initial_pos = None
expanded_grid = {}
expanded_initial_pos = None
direction_map = {"^": -1, ">": 1j, "v": 1, "<": -1j}
with open("day15/input.txt", "r") as f:
    grid_input, instr_input = f.read().split("\n\n")
    for row, line in enumerate(grid_input.split("\n")):
        for col, val in enumerate(line):
            grid[complex(row, col)] = val
            expanded_grid[complex(row, 2 * col)] = val
            expanded_grid[complex(row, 2 * col + 1)] = val
            if val == "@":
                expanded_grid[complex(row, 2 * col + 1)] = "."
                initial_pos = complex(row, col)
                expanded_initial_pos = complex(row, 2 * col)
            elif val == "O":
                expanded_grid[complex(row, 2 * col)] = "["
                expanded_grid[complex(row, 2 * col + 1)] = "]"
    instructions = [direction_map[c] for c in instr_input.replace("\n", "")]


def _attempt_to_move(position: complex, direction: complex):
    

def _get_all_movables(position: complex, direction: complex) -> list[complex]:
    if direction == 1j or direction == -1j:
         return _get_all_horizontal_movables(position, direction)
    
    next_pos = position + direction
    if 

def _get_all_horizontal_movables(position: complex, direction: complex) -> list[complex]:
        next_pos = position + direction
    if next_pos not in expanded_grid:
        return []
    movables = []
    while expanded_grid[next_pos] != ".":
        if expanded_grid[next_pos] == "#":
            return []
        movables.append(next_pos)
        next_pos = next_pos + direction
    return movables


def print_complex_grid_to_file(char_map, file_path):
    """
    Prints a grid based on a mapping of complex numbers to characters and saves it to a file.

    Parameters:
    - char_map: Dictionary mapping complex numbers to characters.
    - file_path: Path to the output text file.
    """
    # Extract row and column bounds from the keys of the char_map
    rows = [int(z.real) for z in char_map.keys()]
    cols = [int(z.imag) for z in char_map.keys()]

    # Determine grid size
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    grid_rows = max_row - min_row + 1
    grid_cols = max_col - min_col + 1

    # Initialize an empty grid with spaces
    grid = [[" " for _ in range(grid_cols)] for _ in range(grid_rows)]

    # Populate the grid with characters from the char_map
    for z, char in char_map.items():
        row = int(z.real)
        col = int(z.imag)
        grid[row][col] = char

    # Write the grid to the file
    with open(file_path, "w") as file:
        for row in grid:
            file.write("".join(row) + "\n")


print_complex_grid_to_file(grid, "day15/grid.txt")
print_complex_grid_to_file(expanded_grid, "day15/expanded_grid.txt")
