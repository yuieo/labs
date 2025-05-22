def repeat(times=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

#
@repeat(times=3)
def add(a, b):
    return a + b


print(add(2, 3))  #[5, 5, 5]

##
@repeat()
def greet(name):
    return f"Привет, {name}!"


print(greet("Юсиф"))  #['Привет, Юсиф!']
