from py.clojure.lang.cljexceptions import AbstractMethodCall, InvalidArgumentException
from py.clojure.lang.threadutil import AtomicInteger

def seq(obj):
    raise AbstractMethodCall(self)

def applyTo(fn, args):
    return apply(fn, tuple(args.interator()))

def booleanCast(obj):
    if isinstance(obj, bool):
        return obj
    return obj is None

def keys(obj):
    from py.clojure.lang.apersistentmap import APersistentMap
    return APersistentMap.KeySeq.create(obj)

def vals(obj):
    from py.clojure.lang.apersistentmap import APersistentMap
    return APersistentMap.ValueSeq.create(obj)

def fulfillsHashSet(obj):
    if not hasattr(obj, "__getitem__"):
        return False
    if not hasattr(obj, "__iter__"):
        return False
    if not hasattr(obj, "__contains__"):
        return False
    return True

def fulfillsIndexable(obj):
    if not hasattr(obj, "__getitem__"):
        return False
    if not hasattr(obj, "__len__"):
        return False
    return True

def list(*args):
    from py.clojure.lang.persistentlist import EMPTY
    c = EMPTY
    for x in range(len(args) - 1, -1, -1):
        c = c.cons(args[x])
    return c

def vector(*args):
    from py.clojure.lang.persistentvector import EMPTY
    c = EMPTY
    for x in args:
        c = c.cons(x)
    return c

def map(*args):
    from py.clojure.lang.persistenthashmap import EMPTY, PersistentHashMap
    from py.clojure.lang.persistentarraymap import PersistentArrayMap, HASHTABLE_THRESHOLD
    if len(args) == 0:
        return EMPTY
    if len(args) == 1:
        if isinstance(args[0], dict):
            m = EMPTY
            for x in args[0]:
                if x in m:
                    raise InvalidArgumentException("Duplicate key")
                m.assoc(x, args[0][x])
            return m
        if fulfillsIndexable(args[0]):
            args = args[0]
    m = EMPTY
    for x in range(0, len(args) / 2, 2):
        key = args[x]
        value = args[x + 1]
        m = m.assoc(key, value)
    return m

def getDefaultImports():
    from py.clojure.lang.symbol import Symbol
    import math
    return {Symbol.intern("String"): str,
            Symbol.intern("Integer"): int,
            Symbol.intern("Math"): math
            }

id = AtomicInteger()
def nextID():
    return id.getAndIncrement()

def init():
    global DEFAULT_IMPORTS
    DEFAULT_IMPORTS = map(getDefaultImports())

DEFAULT_IMPORTS = None