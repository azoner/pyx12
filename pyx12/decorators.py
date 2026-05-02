from __future__ import annotations

import collections.abc
import functools
from collections.abc import Callable
from typing import Any

# See https://wiki.python.org/moin/PythonDecoratorLibrary


def dump_args(func: Callable[..., Any]) -> Callable[..., Any]:
    "This decorator dumps out the arguments passed to a function before calling it"
    argnames = func.__code__.co_varnames[: func.__code__.co_argcount]
    fname = func.__name__

    def echo_func(*args: Any, **kwargs: Any) -> Any:
        print(
            (
                fname,
                ":",
                ", ".join(
                    "%s=%r" % entry for entry in list(zip(argnames, args)) + list(kwargs.items())
                ),
            )
        )
        return func(*args, **kwargs)

    return echo_func


def memoize(obj: Callable[..., Any]) -> Callable[..., Any]:
    cache: dict[Any, Any] = {}
    obj.cache = cache  # type: ignore[attr-defined]

    @functools.wraps(obj)
    def memoizer(*args: Any, **kwargs: Any) -> Any:
        if kwargs:  # frozenset is used to ensure hashability
            key: Any = (args, frozenset(kwargs.items()))
        else:
            key = args
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


class memoized:
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """

    func: Callable[..., Any]
    cache: dict[Any, Any]

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func
        self.cache = {}

    def __call__(self, *args: Any) -> Any:
        if not isinstance(args, collections.abc.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self) -> str:
        """Return the function's docstring."""
        return self.func.__doc__ or ""

    def __get__(self, obj: Any, objtype: Any) -> Callable[..., Any]:
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
