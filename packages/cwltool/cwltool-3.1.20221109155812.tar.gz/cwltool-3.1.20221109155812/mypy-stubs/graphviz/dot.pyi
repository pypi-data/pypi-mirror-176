# Stubs for graphviz.dot (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

from . import files

class Dot(files.File):
    name: Any = ...
    comment: Any = ...
    graph_attr: Any = ...
    node_attr: Any = ...
    edge_attr: Any = ...
    body: Any = ...
    strict: Any = ...
    def __init__(
        self,
        name: Optional[Any] = ...,
        comment: Optional[Any] = ...,
        filename: Optional[Any] = ...,
        directory: Optional[Any] = ...,
        format: Optional[Any] = ...,
        engine: Optional[Any] = ...,
        encoding: Any = ...,
        graph_attr: Optional[Any] = ...,
        node_attr: Optional[Any] = ...,
        edge_attr: Optional[Any] = ...,
        body: Optional[Any] = ...,
        strict: bool = ...,
    ) -> None: ...
    def clear(self, keep_attrs: bool = ...): ...
    def __iter__(self, subgraph: bool = ...): ...
    source: Any = ...
    def node(
        self,
        name,
        label: Optional[Any] = ...,
        _attributes: Optional[Any] = ...,
        **attrs
    ): ...
    def edge(
        self,
        tail_name,
        head_name,
        label: Optional[Any] = ...,
        _attributes: Optional[Any] = ...,
        **attrs
    ): ...
    def edges(self, tail_head_iter): ...
    def attr(
        self, kw: Optional[Any] = ..., _attributes: Optional[Any] = ..., **attrs
    ): ...
    def subgraph(
        self,
        graph: Optional[Any] = ...,
        name: Optional[Any] = ...,
        comment: Optional[Any] = ...,
        graph_attr: Optional[Any] = ...,
        node_attr: Optional[Any] = ...,
        edge_attr: Optional[Any] = ...,
        body: Optional[Any] = ...,
    ): ...

class SubgraphContext:
    parent: Any = ...
    graph: Any = ...
    def __init__(self, parent, kwargs) -> None: ...
    def __enter__(self): ...
    def __exit__(self, type_, value, traceback): ...

class Graph(Dot):
    @property
    def directed(self): ...

class Digraph(Dot):
    @property
    def directed(self): ...
