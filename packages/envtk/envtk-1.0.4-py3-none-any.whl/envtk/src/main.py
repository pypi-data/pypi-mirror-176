from . import sysargs,environ_methods,moduletk


def __help():
    return moduletk.modulestr(environ_methods)
    
def run():
    env_methods = moduletk.module_dict(environ_methods)

    method = sysargs.keymethod(env_methods)
    result = __help()
    if method is not None:
        args_after = sysargs.argsafter(method.__name__)
        if args_after:
            envname = args_after[0]
            if envname:
                result = method(envname)

    print(result)



