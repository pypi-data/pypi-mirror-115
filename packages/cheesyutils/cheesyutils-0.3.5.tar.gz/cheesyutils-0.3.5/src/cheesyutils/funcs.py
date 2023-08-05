from typing import Any, Callable, Iterable


def any_predicate(iterable: Iterable, predicate: Callable[[Any], bool]) -> bool:
    """Returns a boolean if any of the items in `iterable` satisfy the `predicate`
    
    This is similar to python's builtin `any` method except with a customizable predicate

    Parameters
    ----------
    iterable : Iterable
        The iterable object to check
    predicate : Callable(Any)->bool
        The predicate to check against every item of `iterable`. This method must take a sole
        parameter designating the current item to check and return a boolean
    
    Returns
    -------
    A boolean depicting whether an item in `iterable` passed the `predicate` or not
    """

    for item in iterable:
        if predicate(item):
            return True
    
    return False


def all_predicate(iterable: Iterable, predicate: Callable[[Any], bool]) -> bool:
    """Returns a boolean if all of the items in `iterable` satisfy the `predicate`
    
    This is similar to python's builtin `all` method except with a customizable predicate

    Parameters
    ----------
    iterable : Iterable
        The iterable object to check
    predicate : Callable(Any)->bool
        The predicate to check against every item of `iterable`. This method must take a sole
        parameter designating the current item to check and return a boolean
    
    Returns
    -------
    A boolean depicting whether all items in `iterable` passed the `predicate` or not
    """

    for item in iterable:
        if not predicate(item):
            return False
    
    return True
