import networkx as nx

from collections import defaultdict

G = nx.DiGraph()
truth_vals = defaultdict(int)
with open("day24/input.txt", "r") as f:
    given_vals, relations = f.read().strip().split("\n\n")
    for input in given_vals.split("\n"):
        variable_name, truth_val = input.split(":")
        truth_vals[variable_name] = int(truth_val.strip())

    for line in relations.split("\n"):
        input_1, operation, input_2, _, res = line.split(" ")
        combo_node = (input_1, input_2, operation, res)
        G.add_edge(input_1, combo_node)
        G.add_edge(input_2, combo_node)
        G.add_edge(combo_node, res)


def part_1() -> int:
    for node in nx.topological_sort(G):
        if type(node) == tuple:
            input_1, input_2, op, res = node
            truth_vals[res] = _eval_bool_expression(
                truth_vals[input_1], truth_vals[input_2], op
            )
    return sum(int(truth_vals[f"z{i:02}"]) * (2**i) for i in range(100))


def part_2() -> int:
    faulty_nodes = []
    for i in range(100):
        if f"x{i:02}" in G:
            try:
                nx.shortest_path(G, source=f"x{i:02}", target=f"z{i:02}")
                nx.shortest_path(G, source=f"x{i:02}", target=f"z{i+1:02}")
            except nx.NetworkXNoPath:
                faulty_nodes.append(f"x{i:02}")
            try:
                nx.shortest_path(G, source=f"y{i:02}", target=f"z{i:02}")
                nx.shortest_path(G, source=f"y{i:02}", target=f"z{i+1:02}")
            except nx.NetworkXNoPath:
                faulty_nodes.append(f"y{i:02}")
    print(faulty_nodes)


def _eval_bool_expression(input_1: bool, input_2: bool, operation: str):
    match operation:
        case "XOR":
            return input_1 ^ input_2
        case "AND":
            return input_1 and input_2
        case "OR":
            return input_1 or input_2


print(part_2())
