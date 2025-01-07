from itertools import combinations

locks = []
keys = []
with open("day25/input.txt", "r") as f:
    blocks = f.read().strip().split("\n\n")
    for block in blocks:
        block = block.split("\n")
        num_columns = len(block[0])
        counts = [-1] * num_columns

        for row in block:
            for i, char in enumerate(row):
                if char == "#":
                    counts[i] += 1
        if any(block[0][i] == "#" for i in range(len(block[0]))):
            locks.append(counts)
        else:
            keys.append(counts)


def part_1() -> int:
    count = 0
    for lock in locks:
        for key in keys:
            if all(height_1 + height_2 < 6 for height_1, height_2 in zip(lock, key)):
                count += 1
    return count


print(part_1())
