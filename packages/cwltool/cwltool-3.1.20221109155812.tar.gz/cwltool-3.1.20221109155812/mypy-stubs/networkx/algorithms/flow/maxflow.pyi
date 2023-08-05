# Stubs for networkx.algorithms.flow.maxflow (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

from .preflowpush import preflow_push

default_flow_func = preflow_push

def maximum_flow(
    flowG, _s, _t, capacity: str = ..., flow_func: Optional[Any] = ..., **kwargs
): ...
def maximum_flow_value(
    flowG, _s, _t, capacity: str = ..., flow_func: Optional[Any] = ..., **kwargs
): ...
def minimum_cut(
    flowG, _s, _t, capacity: str = ..., flow_func: Optional[Any] = ..., **kwargs
): ...
def minimum_cut_value(
    flowG, _s, _t, capacity: str = ..., flow_func: Optional[Any] = ..., **kwargs
): ...
