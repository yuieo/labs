# c рекурсии
def recursive_xi(i):
    if i == 1:
        return 1
    if i == 2:
        return -1 / 8

    # x_i = ((i-1)*x_{i-1})/3 + ((i-2)*x_{i-2})/4
    return ((i - 1) * recursive_xi(i - 1)) / 3 + ((i - 2) * recursive_xi(i - 2)) / 4

print("c рекурсии")
if __name__ == "__main__":
    for i in range(1, 6):
        print(f"x[{i}] = {round(recursive_xi(i), 6)}")


# c рекурсии
def iterative_xi(i):
    if i < 1:
        raise ValueError("i должно быть положительным числом")
    if i == 1:
        return 1
    if i == 2:
        return -1 / 8

    x_prev_prev = 1
    x_prev = -1 / 8

    for n in range(3, i + 1):
        x_current = ((n - 1) * x_prev) / 3 + ((n - 2) * x_prev_prev) / 4
        x_prev_prev = x_prev
        x_prev = x_current

    return x_current


print("без рекурсии")
if __name__ == "__main__":
    for i in range(1, 6):
        print(f"x[{i}] = {round(iterative_xi(i), 6)}")