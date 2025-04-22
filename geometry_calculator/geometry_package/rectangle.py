import math


class Rectangle:
    @staticmethod
    def area(a, b):
        return a * b

    @staticmethod
    def circumradius(a, b):
        return math.sqrt(a ** 2 + b ** 2) / 2

    @staticmethod
    def inradius(a, b):
        return "У прямоугольника нет вписанной окружности, если это не квадрат"