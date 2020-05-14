from enum import Enum

def is_elemental(obj):
    return isinstance(obj, (type(None), int, float, bool))

def is_collection(obj):
    return isinstance(obj, (list, dict, tuple, set, frozenset))

def is_customized_class(obj):
    if is_elemental(obj) or is_collection(obj):
        return False
    if (hasattr(obj, '__dict__') or hasattr(obj, '__slots__')) and obj.__module__ != 'builtins':
        return True
    return False