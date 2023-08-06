from typing import Any, Callable, TypeVar

__all__ = ['cached', 'cached_method']

# type variable for "cached"
TCache = TypeVar('TCache')

def cached(func: Callable[..., TCache]) -> Callable[..., TCache]:
    'Returns a function that caches its results.'
    result = uncached = object()
    def wrapper(*args, **kwargs) -> Any:
        nonlocal result
        if result is uncached:
            result = func(*args, **kwargs)
        return result
    return wrapper

def cached_method(func: Callable[..., TCache]) -> Callable[..., TCache]:
    'Returns a function that caches its result by the first parameter.'
    result = {}
    def wrapper(*args, **kwargs) -> Any:
        if args[0] in result:
            return result[args[0]]
        r = func(*args, **kwargs)
        result[args[0]] = r
        return r
    return wrapper
        