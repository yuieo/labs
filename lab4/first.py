def logger(func=None, *, verbose=True):
    if func is not None:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if verbose and not kwargs.get('_recursive', False):
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
    def calculator(number, _recursive=False):
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


def recursive_example(n):
    calc = make_calc("+")
    if n == 0:
        return calc(0, _recursive=True)
    return calc(n + recursive_example(n-1), _recursive=(n >= 1))


print('рекурсия от n до 0')
n = recursive_example(4)  # 10
print(n)
