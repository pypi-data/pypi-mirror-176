# Stubs for networkx.algorithms.connectivity.connectivity (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

from networkx.algorithms.flow import edmonds_karp

default_flow_func = edmonds_karp

def local_node_connectivity(
    G,
    s,
    t,
    flow_func: Optional[Any] = ...,
    auxiliary: Optional[Any] = ...,
    residual: Optional[Any] = ...,
    cutoff: Optional[Any] = ...,
): ...
def node_connectivity(
    G, s: Optional[Any] = ..., t: Optional[Any] = ..., flow_func: Optional[Any] = ...
): ...
def average_node_connectivity(G, flow_func: Optional[Any] = ...): ...
def all_pairs_node_connectivity(
    G, nbunch: Optional[Any] = ..., flow_func: Optional[Any] = ...
): ...
def local_edge_connectivity(
    G,
    s,
    t,
    flow_func: Optional[Any] = ...,
    auxiliary: Optional[Any] = ...,
    residual: Optional[Any] = ...,
    cutoff: Optional[Any] = ...,
): ...
def edge_connectivity(
    G,
    s: Optional[Any] = ...,
    t: Optional[Any] = ...,
    flow_func: Optional[Any] = ...,
    cutoff: Optional[Any] = ...,
): ...
