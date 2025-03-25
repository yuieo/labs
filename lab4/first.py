def repeat(times):
    def decorator(func):
        def wrapper(arg):
            results = []
            for _ in range(times):
                result = func(arg)
                results.append(result)
            return results
        return wrapper
    return decorator

def make_calc(operation, initial=0):
    result = initial  # начальное значение сохраняется в замыкании
    
    def calculator(value):
        nonlocal result  # позволяет менять значение из замыкания
        
        if operation == "+":
            result += value
        elif operation == "-":
            result -= value
        elif operation == "*":
            result *= value
        elif operation == "/":
            result /= value
            
        return result
    
    return calculator

calc = make_calc("*", initial=1)

calc = repeat(3)(calc)

# Тест
print(calc(5)) 
print(calc(2))
