def repeat(times=1):
    def decorator(func):
        func.is_repeating = False  # флаг для отслеживания повторных вызовов

        def wrapper(*args, **kwargs):
            if func.is_repeating:
                # если это рекурсивный вызов, просто выполняем функцию
                return func(*args, **kwargs)

            func.is_repeating = True
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            func.is_repeating = False
            return results

        return wrapper

    return decorator


# Примеры с рекурсивной функцией
@repeat(times=2)
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


print(factorial(5))  # [120, 120] (декоратор применяется только к внешнему вызову)


@repeat(times=3)
def square(x):
    return x ** 2

print(square(4))


@repeat(times=5)
def get_random_number():
    import random
    return random.randint(1, 76)

print(get_random_number())
