from functools import wraps
from typing import Callable, Any, Optional


def repeat(times: Optional[int] = 1):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> list[Any]:
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results

        return wrapper

    return decorator


@repeat(times=3)
def add(a: int, b: int) -> int:
    return a + b


print(add(2, 3))


@repeat()
def greet(name: str) -> str:
    return f"Привет, {name}!"


print(greet("Юсиф"))
