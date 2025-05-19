from main import filtered_random_generator
from main import count_divisors

def test_filtered_random_generator_basic():
    min_val = 1
    max_val = 100
    max_div = 4
    count = 10
    result = filtered_random_generator(min_val, max_val, max_div, count)

    # Проверяем количество чисел
    assert len(result) == count

    # Проверяем диапазон и количество делителей
    for num in result:
        assert min_val <= num <= max_val
        assert count_divisors(num) <= max_div


def test_single_value():
    # Проверяем случай, когда min и max совпадают
    result = filtered_random_generator(5, 5, max_divisors=2, count=3)
    assert len(result) == 3
    for num in result:
        assert num == 5
        assert count_divisors(5) <= 2  # 5 — простое число (2 делителя)


def test_edge_cases():
    # Проверяем граничные значения диапазона
    result = filtered_random_generator(2, 2, max_divisors=2, count=5)
    assert all(num == 2 for num in result)
    assert count_divisors(2) == 2  # Простое число
