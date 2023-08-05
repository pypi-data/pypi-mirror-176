# Stubs for networkx.readwrite.adjlist (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def generate_adjlist(G, delimiter: str = ...): ...
def write_adjlist(
    G, path, comments: str = ..., delimiter: str = ..., encoding: str = ...
): ...
def parse_adjlist(
    lines,
    comments: str = ...,
    delimiter: Optional[Any] = ...,
    create_using: Optional[Any] = ...,
    nodetype: Optional[Any] = ...,
): ...
def read_adjlist(
    path,
    comments: str = ...,
    delimiter: Optional[Any] = ...,
    create_using: Optional[Any] = ...,
    nodetype: Optional[Any] = ...,
    encoding: str = ...,
): ...
