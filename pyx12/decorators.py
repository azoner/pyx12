def dump_args(func):
    "This decorator dumps out the arguments passed to a function before calling it"
    argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
    fname = func.__name__

    def echo_func(*args, **kwargs):
        print((fname, ":", ', '.join('%s=%r' % entry
            for entry in list(zip(argnames, args)) + list(kwargs.items()))))
        return func(*args, **kwargs)

    return echo_func
