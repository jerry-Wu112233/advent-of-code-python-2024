import networkx as nx

obstacles = set()
width = 71
height = 71
coords_after_1024 = []
with open("day18/input.txt", "r") as f:
    for line_num, line in enumerate(f.read().strip().split("\n")):
        x_coord, y_coord = map(int, line.rstrip("\n").split(","))
        if line_num >= 1024:
            coords_after_1024.append(complex(y_coord, x_coord))
            continue
        obstacles.add(complex(y_coord, x_coord))

G = nx.Graph()

directions = [-1, 1, -1j, 1j]
for row in range(width):
    for col in range(height):
        pos = complex(row, col)
        if pos in obstacles:
            continue
        for dir in directions:
            neighbor = pos + dir
            if not (0 <= neighbor.real < width and 0 <= neighbor.imag < height):
                continue
            if neighbor in obstacles:
                continue
            G.add_edge(pos, neighbor)


def part_1() -> int:
    return nx.shortest_path_length(
        G, source=complex(0, 0), target=complex(width - 1, height - 1)
    )


def part_2() -> tuple[int, int]:
    for obstacle in coords_after_1024:
        for dir in directions:
            neighbor = obstacle + dir
            try:
                G.remove_edge(obstacle, neighbor)
            except nx.NetworkXError:
                continue
            obstacles.add(obstacle)
        try:
            nx.shortest_path_length(
                G, source=complex(0, 0), target=complex(width - 1, height - 1)
            )
        except nx.NetworkXNoPath:
            return obstacle.imag, obstacle.real
    return 0, 0
