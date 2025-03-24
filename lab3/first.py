# без рекурсии
def count_iterative(lst):
    count = 0
    stack = [lst]

    while stack:
        current = stack.pop()
        for item in current:
            if isinstance(item, list):
                count += 1
                stack.append(item)
            else:
                count += 1
    return count


# с рекурсией
def count_recursive(lst):
    count = 0
    for item in lst:
        if isinstance(item, list):
            count += 1
            count += count_recursive(item)
        else:
            count += 1
    return count


test_cases = [
    [],
    [1, [2, 3]],
    ["x", "y", ["z"]],
    [1, 2, [3, 4, [5]]],
    [1, 2, 4, ["z", "x"]]
]

for test in test_cases:
    print(f"пример: {test}")
    print(f"без рекурсии: {count_iterative(test)}")
    print(f"с рекурсией: {count_recursive(test)}")
    print()
