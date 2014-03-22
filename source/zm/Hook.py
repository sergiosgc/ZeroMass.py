import inspect
import zm
def Hook(fn):
    members = dict(inspect.getmembers(fn))
    hookName = "%s.%s" % (members['__module__'], members['__qualname__'])
    del members
    def inner(*args, **kwargs):
        (func, args, kwargs) = zm.ZM().hookPre(hookName, (fn, args, kwargs))
        return zm.ZM().hookPost(hookName, (func(*args, **kwargs), args, kwargs))
    return inner

def HookBefore(targetHook):
    def decorate(f):
        zm.ZM().registerPreHook(targetHook, f)
        return f
    return decorate

def HookAfter(targetHook):
    def decorate(f):
        zm.ZM().registerPostHook(targetHook, f)
        return f
    return decorate

