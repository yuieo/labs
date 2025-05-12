from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """Базовый класс для всех фигур"""

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def circumradius(self):
        pass

    @abstractmethod
    def inradius(self):
        pass

    def __str__(self):
        return f"Фигура: {self.__class__.__name__}"

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value <= 0:
            raise ValueError("Сторона a должна быть положительной")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError("Сторона b должна быть положительной")
        self._b = value

    def area(self):
        return self.a * self.b

    def circumradius(self):
        return math.sqrt(self.a ** 2 + self.b ** 2) / 2

    def inradius(self):
        if self.a == self.b:
            return self.a / 2
        return "Нет вписанной окружности"

    def __eq__(self, other):
        return isinstance(other, Rectangle) and self.a == other.a and self.b == other.b

    def __repr__(self):
        return f"Rectangle(a={self.a}, b={self.b})"


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Стороны не образуют треугольник")

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value <= 0:
            raise ValueError("Сторона a должна быть положительной")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError("Сторона b должна быть положительной")
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        if value <= 0:
            raise ValueError("Сторона c должна быть положительной")
        self._c = value

    def area(self):
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def circumradius(self):
        return (self.a * self.b * self.c) / (4 * self.area())

    def inradius(self):
        return self.area() / ((self.a + self.b + self.c) / 2)

    def __eq__(self, other):
        return isinstance(other, Triangle) and (self.a, self.b, self.c) == (other.a, other.b, other.c)

    def __lt__(self, other):
        return self.area() < other.area()


class Trapezoid(Shape):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        if a == b:
            raise ValueError("Основания трапеции не могут быть равны")

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value <= 0:
            raise ValueError("Основание a должно быть положительным")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError("Основание b должно быть положительным")
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        if value <= 0:
            raise ValueError("Боковая сторона c должна быть положительной")
        self._c = value

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        if value <= 0:
            raise ValueError("Боковая сторона d должна быть положительной")
        self._d = value

    def area(self):
        return (self.a + self.b) / 2 * math.sqrt(self.c ** 2 - ((self.b - self.a) ** 2) / 4)

    def circumradius(self):
        if self.c != self.d:
            return "Только для равнобедренной трапеции"
        return math.sqrt(self.a * self.b + self.c ** 2) / 2

    def inradius(self):
        if abs((self.a + self.b) - (self.c + self.d)) > 1e-6:
            return "Невозможно вписать окружность"
        return self.area() / ((self.a + self.b) / 2)

    def __eq__(self, other):
        return isinstance(other, Trapezoid) and (self.a, self.b, self.c, self.d) == (other.a, other.b, other.c, other.d)

    def __bool__(self):
        return self.area() > 0



#str
# rect = Rectangle(4, 5)
# print(rect)

#eq
# rect1 = Rectangle(3, 4)
# rect2 = Rectangle(3, 4)
# rect3 = Rectangle(5, 6)
# print(rect1 == rect2)
# print(rect1 == rect3)

#lt
# tri1 = Triangle(3, 4, 5)  # ~6
# tri2 = Triangle(5, 5, 5)  # ~11
# print(tri1 < tri2)
