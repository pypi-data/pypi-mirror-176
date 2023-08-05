import sys
from typing import TypeVar,Callable
T = TypeVar("T")

def __arglist(__sysargs:list[str]=None):
    return (sys.argv if __sysargs is None else __sysargs)

def __index(__key:str,sysargs:list[str]=None):
    return __arglist(sysargs).index(__key)

def keyarg(__keys:dict,sysargs:list[str]=None,default:str | None=None):
    return next((arg for arg in __arglist(sysargs) if arg in __keys),default)


def keymethod(__keys:dict,sysargs:list[str]=None,default:str | Callable | None = None):
    key = keyarg(__keys,sysargs=sysargs)
    if key is None:
        if isinstance(default,str):
            method = __keys[default]
        elif isinstance(default,Callable):
            method = default
        else:
            method = None
    else:
        method = __keys[key]
    return method
    


def argsafter(__key:str,sysargs:list[str]=None):
    sa = __arglist(sysargs)
    i = __index(__key,sysargs=sa)

    if i < len(sa):
        sa = sa[i+1:]
    return sa


