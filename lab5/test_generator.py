from main import count_divisors

def test_count_divisors():
    assert count_divisors(0) == 0
    assert count_divisors(1) == 1
    assert count_divisors(7) == 2   # Простое число (делители: 1, 7)
    assert count_divisors(4) == 3    # Квадрат простого (делители: 1, 2, 4)
    assert count_divisors(6) == 4    # Составное число (делители: 1, 2, 3, 6)
    assert count_divisors(12) == 6   # Делители: 1, 2, 3, 4, 6, 12
