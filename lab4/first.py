def logger(func=None, *, verbose=True):
    if func is not None:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if verbose:
                print(f"Текущий результат: {result}")
            return result
        return wrapper
    else:
        def decorator(f):
            return logger(f, verbose=verbose)
        return decorator


def make_calc(operation, initial=0):
    result = initial

    @logger(verbose=True)
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


calc1 = make_calc("*", initial=1)
calc1(5)  # 5
calc1(2)  # 10

calc2 = make_calc("+", initial=0)
calc2(3)  # 3
calc2(4)  # 7
