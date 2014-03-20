import inspect
def Hook(fn):
    members = dict(inspect.getmembers(fn))

    print(members['__module__'] + "." + members['__qualname__'])


    print("Initializing")
    stack = inspect.stack()
    print(inspect.getmodule(stack[1][0]))
    print(fn.__name__)
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)
    return inner

