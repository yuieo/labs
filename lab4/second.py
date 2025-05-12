def repeat(_func=None, *, times=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator if _func is None else decorator(_func)



@repeat(times=6)
def hello(name):
    return f"Привет, {name}"

print(hello(""))
