def logger(func):
    def wrapper(*args):
        result = func(*args)
        print(f"Текущий результат: {result}")
        return result

    return wrapper


def make_calc(operation, initial=0):
    result = initial

    @logger
    def calculator(number):
        nonlocal result


        if operation == "+":
            result += number
        elif operation == "-":
            result -= number
        elif operation == "*":
            result *= number
        elif operation == "/":
            result /= number

        return result

    return calculator



calc = make_calc("*", initial=1)
print(calc(5))
print(calc(2))

calc = make_calc("*", initial=1)
calc(5)
calc(2)

calc2 = make_calc("+", initial=0)
calc2(3)
calc2(4)

calc3 = make_calc("-", initial=10)
calc3(3)
calc3(2)