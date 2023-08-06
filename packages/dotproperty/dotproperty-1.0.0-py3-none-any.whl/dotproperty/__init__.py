"""
dotprop

abbreviations:

    __k: key (str)
    __v: value (object)
    __kl: keys (list[str]);(keys list)
    __o: object
    __s: str
    __dotpath: str (str.str.str...);(config.package.name)

"""
from functools import reduce as __reduce

__dotsplit_base = lambda __s: __s.split(".") if "." in __s else [__s]
__dotsplit = lambda __s: [v for v in __dotsplit_base(__s) if v]

__isdict = lambda __o: isinstance(__o, dict)

__oget = lambda __o: dict.__getitem__ if __isdict(__o) else getattr
__oset = lambda __o: dict.__setitem__ if __isdict(__o) else setattr

__safeget = lambda __o, __k: __oget(__o)(__o, __k)
__safeset = lambda __o, __k, __v: __oset(__o)(__o, __k, __v)

__reduce_getset = lambda __o, __k: (__o := __safeget(__o, __k))


def __seqset(__o, __kl: list[str], __v):
    obj, storage = __o, []
    append = storage.append
    for key in __kl[:-1]:
        append((obj, key))
        obj = __safeget(obj, key)
    __safeset(obj, __kl[-1], __v)
    result = obj
    for (stored_obj, key) in reversed(storage):
        __safeset(stored_obj, key, result)
        result = stored_obj


__fget = lambda __kl: lambda __o: __reduce(__reduce_getset, __kl, __o)
__fset = lambda __kl: lambda __o, __v: __seqset(__o, __kl, __v)
__keys2dotprop = lambda __kl: property(fget=__fget(__kl), fset=__fset(__kl))
__dotprop = lambda __s: __keys2dotprop(__dotsplit(__s))


def dotprop(__dotpath: str):
    return __dotprop(__dotpath)
