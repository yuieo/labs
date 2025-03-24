def repeat(times):
    def decorator(func):
        def wrapper(*args):
            results = []
            for _ in range(times):
                result = func(*args)
                results.append(result)
            return results
        return wrapper
    return decorator


def create_counter():
    count = 0
    @repeat(11)
    def counter():
        nonlocal count
        count += 1
        return count
    return counter


my_counter = create_counter()
print(my_counter())