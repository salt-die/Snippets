"""Subclass QGraph for fast networkx graph creation -- similar to the `from_dict_of_lists` constructor, but
with fewer commas and brackets, example:

class MyGraph(QGraph, directed=False):
    a: [b, c]
    b: [d, e, f]
    g: []

g = MyGraph()
"""


import networkx as nx


class Nodes(dict):
    def __init__(self, directed=True):
        super().__init__()

    def __missing__(self, key):
        if key.startswith('__'): raise KeyError(key)
        self[key] = key
        return key


_directed = {}
class QGraphMeta(type):
    def __prepare__(name, bases, **kwargs):
        _directed[name] = kwargs.get('directed', True)
        return Nodes()

    def __call__(cls):
        G = nx.DiGraph if _directed[cls.__name__] else nx.Graph
        return nx.from_dict_of_lists(cls.__dict__['__annotations__'], create_using=G)


class QGraph(metaclass=QGraphMeta):
    def __init_subclass__(*args, **kwargs):
        pass
