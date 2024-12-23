from collections import defaultdict

with open("day22/input.txt", "r") as f:
    secret_nums = list(map(int, f.read().strip().split("\n")))


def part_1() -> int:
    res = 0
    for secret_num in secret_nums:
        for _ in range(2000):
            secret_num = mix_and_prune(secret_num)
        res += secret_num
    return res


def part_2() -> int:
    reward_map = defaultdict(int)
    for secret_num in secret_nums:
        last_digits = []
        for _ in range(2000):
            last_digits.append(secret_num % 10)
            secret_num = mix_and_prune(secret_num)
        last_digits.append(secret_num % 10)
        differences = [
            second_term - first_term
            for first_term, second_term in zip(last_digits, last_digits[1:])
        ]
        visited = set()
        for i in range(len(differences) - 3):
            if tuple(differences[i : i + 4]) in visited:
                continue
            reward_map[tuple(differences[i : i + 4])] += last_digits[i + 4]
            visited.add(tuple(differences[i : i + 4]))

    return max(reward_map.values())


def mix_and_prune(num: int) -> int:
    num ^= num * 64
    num %= 16777216

    num ^= num >> 5
    num %= 16777216

    num ^= num * 2048
    return num % 16777216
