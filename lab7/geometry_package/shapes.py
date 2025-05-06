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
            raise ValueError("Длина стороны должна быть > 0")
        self._a =  value

    @property
    def b(self):
        return self._b
    
    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError
        self._b =  value

    def area(self):
        return self.a * self.b

    def circumradius(self):
        return math.sqrt(self.a ** 2 + self.b ** 2) / 2

    def inradius(self):
        if self.a == self.b:
            return self.a / 2
        return "Нет вписанной окружности"
    
    def __str__(self):
        return f"Прямоугольник: a={self.a}, b={self.b}"
    def __repr__(self):
        return f"Rectangle(a={self.a}, b={self.b})"


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def circumradius(self):
        return (self.a * self.b * self.c) / (4 * self.area())

    def inradius(self):
        return self.area() / ((self.a + self.b + self.c) / 2)
    def __str__(self):
        return f"Треугольник: a={self.a}, b={self.b}, c={self.c}"
    def __repr__(self):
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"



class Trapezoid(Shape):
    def __init__(self, a, b, c, d):
        self.a = a  # осн
        self.b = b  # осн
        self.c = c  # бок
        self.d = d  # бок

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
    def __str__(self):
        return f"Трапеция: a={self.a}, b={self.b}, c={self.c}, d={self.d}"
    def __repr__(self):
        return f"Trapezoid(a={self.a}, b={self.b}, c={self.c}, d={self.d})"
