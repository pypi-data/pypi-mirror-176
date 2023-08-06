from some_crap.version import __version__

def exposed_function(func, *args, **kwargs):
    return func(*args, **kwargs)
