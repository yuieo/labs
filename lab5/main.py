import time


def simple_random_generator(seed=None, a=1664525, c=1013904223, m=2 ** 32):
    """Линейный конгруэнтный генератор случайных чисел"""
    if seed is None:
        seed = int(time.time() * 1000) % m
    current = seed
    while True:
        current = (a * current + c) % m
        yield current # функция приостанавливается здесь и возвращает current


def count_divisors(num):
    """Функция для подсчета количества делителей числа"""
    if num == 0:
        return 0
    if num == 1:
        return 1

    count = 2  # 1 и само число
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            if i == num // i:
                count += 1
            else:
                count += 2
    return count


def filtered_random_generator(min_val, max_val, max_divisors, count=10):
    """Генератор случайных чисел в диапазоне [min_val, max_val],
    отфильтрованных по максимальному количеству делителей"""
    rng = simple_random_generator()
    numbers_in_range = map(lambda x: min_val + x % (max_val - min_val + 1), rng) # Преобразует числа из ЛКГ в диапазон (x = 1015568748 → 1 + 1015568748 % 100 → 1 + 48 = 49)
    filtered_numbers = filter(lambda x: count_divisors(x) <= max_divisors, numbers_in_range)
    result = []
    for num in filtered_numbers:
        result.append(num)
        if len(result) >= count:
            break
    return result

if __name__ == "__main__":
    min_value = 1
    max_value = 100
    max_divisors_count = 4
    numbers_count = 11

    result_numbers = filtered_random_generator(min_value, max_value, max_divisors_count, numbers_count)

    print(f"Сгенерированные числа с количеством делителей не более {max_divisors_count}:")
    for num in result_numbers:
        divisors = count_divisors(num)
        print(f"Число: {num}, делители: {divisors}")
