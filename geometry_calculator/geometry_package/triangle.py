import math


class Triangle:
    @staticmethod
    def area(a, b, c):
        p = (a + b + c) / 2
        return math.sqrt(p * (p - a) * (p - b) * (p - c))

    @staticmethod
    def circumradius(a, b, c):
        area = Triangle.area(a, b, c)
        return (a * b * c) / (4 * area)

    @staticmethod
    def inradius(a, b, c):
        p = (a + b + c) / 2
        area = Triangle.area(a, b, c)
        return area / p