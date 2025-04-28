import itertools
import doctest


class CodeGenerator:
    """
    Класс для решения задачи о генерации 5-буквенных кодов с определенными ограничениями.

    Метод solve() возвращает количество допустимых кодов.

    Доктест:
    >>> CodeGenerator().solve()
    10476
    """

    def __init__(self):
        self.letters = 'ТИМОФЕЙ'
        self.code_length = 5

    def is_valid_code(self, code):
        """Проверяет, удовлетворяет ли код всем условиям."""
        if code.count('Й') > 1:
            return False
        if code[0] == 'Й' or code[-1] == 'Й':
            return False
        if 'ЙИ' in ''.join(code) or 'ИЙ' in ''.join(code):
            return False
        return True

    def solve(self):
        """Возвращает количество допустимых кодов."""
        count = 0
        for code in itertools.product(self.letters, repeat=self.code_length):
            if self.is_valid_code(code):
                count += 1
        return count


class BinaryOnesCounter:
    """
    Класс для подсчета количества единиц в двоичной записи выражения 4^2020 + 2^2017 - 15.

    Метод solve() возвращает количество единиц в двоичном представлении результата.

    Доктест:
    >>> BinaryOnesCounter().solve()
    2015
    """

    def __init__(self):
        self.exponent1 = 2020
        self.exponent2 = 2017
        self.subtractor = 15

    def solve(self):
        """Вычисляет выражение и возвращает количество единиц в его двоичном представлении."""
        result = 4 ** self.exponent1 + 2 ** self.exponent2 - self.subtractor
        return bin(result).count('1')


class PrimeDivisorsFinder:
    """
    Класс для поиска чисел в заданном диапазоне, имеющих ровно два простых делителя.

    Метод solve() возвращает список кортежей с найденными числами и их делителями.

    Доктест:
    >>> PrimeDivisorsFinder(5, 9).solve()
    [(6, (2, 3)), (8, (2, 4))]
    """

    def __init__(self, start=174457, end=174505):
        self.start = start
        self.end = end

    def find_divisors(self, n):
        """Находит все делители числа n, кроме 1 и самого числа."""
        divisors = []
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                if d == n // d:
                    divisors.append(d)
                else:
                    divisors.extend([d, n // d])
                if len(divisors) > 2:
                    break
        return sorted(divisors)

    def solve(self):
        """Возвращает список кортежей (число, (делитель1, делитель2)) для чисел с ровно двумя делителями."""
        result = []
        for n in range(self.start, self.end + 1):
            divisors = self.find_divisors(n)
            if len(divisors) == 2:
                result.append((n, (divisors[0], divisors[1])))
        return result


if __name__ == "__main__":
    doctest.testmod()

    print("Задание 1:")
    print(CodeGenerator().solve())

    print("\nЗадание 2:")
    print(BinaryOnesCounter().solve())

    print("\nЗадание 3:")
    for number, divisors in PrimeDivisorsFinder().solve():
        print(divisors[0], divisors[1])
