from itertools import groupby, islice, zip_longest

with open("day9/input.txt", "r") as f:
    disk_map = [int(n) for line in f for n in line.rstrip("\n")]


class Block:
    def __init__(self, val, start, length):
        self.val = val
        self.start = start
        self.end = start + length - 1
        self.length = length


def part_1() -> int:
    file_blocks = _disk_map_to_file_blocks()
    for space_index, block_index in zip(
        _disk_map_indices(find_space=True),
        reversed(_disk_map_indices(find_space=False)),
    ):
        if block_index < space_index:
            break
        file_blocks[space_index] = file_blocks[block_index]
        file_blocks[block_index] = "."

    return sum(i * int(val) for i, val in enumerate(file_blocks) if val != ".")


def part_2() -> int:
    file_blocks = _disk_map_to_file_blocks()
    condensed_repr_of_blocks = _groupby_with_indices(file_blocks)
    for block in reversed(condensed_repr_of_blocks):
        if block.val == ".":
            continue
        for space_block in filter(lambda t: t.val == ".", condensed_repr_of_blocks):
            if space_block.start > block.start:
                break
            if space_block.length < block.length:
                continue
            file_blocks[space_block.start : space_block.start + block.length] = [
                block.val for _ in range(block.length)
            ]
            file_blocks[block.start : block.end + 1] = [
                "." for _ in range(block.length)
            ]
            space_block.length -= block.length
            space_block.start += block.length
            break
    return sum(i * int(val) for i, val in enumerate(file_blocks) if val != ".")


def _groupby_with_indices(s: list[str]) -> list[Block]:
    result = []
    start = 0
    for char, group in groupby(s):
        length = len(list(group))
        result.append(Block(char, start, length))
        start += length
    return result


def _disk_map_indices(find_space: bool) -> list[int]:
    file_blocks = _disk_map_to_file_blocks()
    if find_space:
        return [i for i, val in enumerate(file_blocks) if val == "."]
    return [i for i, val in enumerate(file_blocks) if val != "."]


def _disk_map_to_file_blocks() -> list[str]:
    blocks = [
        (str(id_num), repetitions)
        for id_num, repetitions in enumerate(islice(disk_map, 0, None, 2))
    ]
    spaces = [(".", repetitions) for repetitions in islice(disk_map, 1, None, 2)]
    file_blocks = []
    for pair in zip_longest(blocks, spaces, fillvalue=(".", 0)):
        for symbol, repetitions in pair:
            file_blocks.extend([symbol] * repetitions)
    return file_blocks
