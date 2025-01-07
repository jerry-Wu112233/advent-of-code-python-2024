from collections import Counter

left_arr = []
right_arr = []
num_counter = Counter()
with open("day1/input.txt", "r") as f:
    for line in f:
        arr = line.split("   ")
        num1 = arr[0]
        num2 = arr[1]
        left_arr.append(int(num1))
        right_arr.append(int(num2))
        num_counter[int(num2)] += 1

left_arr.sort()
right_arr.sort()
diff_sum = 0
sim_score = 0

for i in range(len(left_arr)):
    diff_sum += abs(left_arr[i] - right_arr[i])
    sim_score += num_counter[left_arr[i]] * left_arr[i]
print(diff_sum)
print(sim_score)
