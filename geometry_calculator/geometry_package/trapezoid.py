import math


class Trapezoid:
    @staticmethod
    def area(a, b, c, d):
        h = math.sqrt(c ** 2 - (((a - b) ** 2 + c ** 2 - d ** 2) / (2 * (a - b))) ** 2)
        return (a + b) * h / 2

    @staticmethod
    def circumradius(a, b, c, d):
        return "Для трапеции нет универсальной формулы описанной окружности"

    @staticmethod
    def inradius(a, b, c, d):
        return "У трапеции нет вписанной окружности, если не выполняется условие a + c = b + d"