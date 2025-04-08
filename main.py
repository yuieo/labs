import time

def simple_random(min_val, max_val):
    seed = simple_random.seed
    seed = (1664525 * seed + 1013904223) & 0xFFFFFFFF
    simple_random.seed = seed
    return min_val + (seed % (max_val - min_val + 1))

simple_random.seed = int(time.time())

def count_divisors(num):
    if num < 1:
        return 0
    count = 0
    for i in range(1, int(num**0.5) + 1):
        if num % i == 0:
            count += 1
            if i != num // i:
                count += 1
    return count

def generate_numbers(min_val, max_val, count):
    for _ in range(count):
        yield simple_random(min_val, max_val)

min_val = 1
max_val = 500
n = 4
count = 10

numbers_generator = generate_numbers(min_val, max_val, count)
numbers = list(numbers_generator)


filtered_numbers = list(filter(lambda x: count_divisors(x) <= n, numbers))

print("Сгенерированные числа:", numbers)
print("После фильтрации:", filtered_numbers)
