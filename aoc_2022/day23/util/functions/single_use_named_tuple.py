from collections import namedtuple

def single_use_named_tuple(name, **fields):
    return namedtuple(name,fields)(*fields.values())