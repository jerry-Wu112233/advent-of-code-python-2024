import networkx as nx

pairs = []
with open("day23/input.txt", "r") as f:
    for line in f.read().strip().split("\n"):
        pairs.append(line.split("-"))

G = nx.Graph()
for comp_1, comp_2 in pairs:
    G.add_edge(comp_1, comp_2)


def part_1() -> int:
    computer_count = 0
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) != 3:
            continue
        if any("t" == comp[0] for comp in clique):
            computer_count += 1
    return computer_count


def part_2() -> str:
    max_size_clique = max(list(nx.find_cliques(G)), key=len)
    return ",".join(node for node in sorted(max_size_clique))
