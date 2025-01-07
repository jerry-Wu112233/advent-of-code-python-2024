safe_count = 0
with open("day2/input.txt", "r") as f:
    for line in f:
        is_increasing = True
        arr = line.split(" ")
        for i, val in enumerate(arr):
            arr[i] = int(val)
        faulty_index = None
        is_decreasing_and_diff_enough = all(
            arr[i - 1] < arr[i] and 1 <= abs(arr[i - 1] - arr[i]) <= 3
            for i in range(1, len(arr))
        )
        is_increasing_and_diff_enough = all(
            arr[i - 1] > arr[i] and 1 <= abs(arr[i - 1] - arr[i]) <= 3
            for i in range(1, len(arr))
        )

        for index in range(len(arr)):
            new_arr = arr[:index] + arr[index + 1 :]
            is_decreasing_and_diff_enough = all(
                new_arr[i - 1] > new_arr[i]
                and 1 <= abs(new_arr[i - 1] - new_arr[i]) <= 3
                for i in range(1, len(new_arr))
            )
            is_increasing_and_diff_enough = all(
                new_arr[i - 1] < new_arr[i]
                and 1 <= abs(new_arr[i - 1] - new_arr[i]) <= 3
                for i in range(1, len(new_arr))
            )

            if is_decreasing_and_diff_enough or is_increasing_and_diff_enough:
                safe_count += 1
                break

print(safe_count)
