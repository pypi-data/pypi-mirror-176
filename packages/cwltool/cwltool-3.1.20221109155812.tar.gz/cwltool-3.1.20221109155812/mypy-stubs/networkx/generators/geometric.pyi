# Stubs for networkx.generators.geometric (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def random_geometric_graph(
    n, radius, dim: int = ..., pos: Optional[Any] = ..., p: int = ...
): ...
def soft_random_geometric_graph(
    n,
    radius,
    dim: int = ...,
    pos: Optional[Any] = ...,
    p: int = ...,
    p_dist: Optional[Any] = ...,
): ...
def geographical_threshold_graph(
    n,
    theta,
    dim: int = ...,
    pos: Optional[Any] = ...,
    weight: Optional[Any] = ...,
    metric: Optional[Any] = ...,
    p_dist: Optional[Any] = ...,
): ...
def waxman_graph(
    n,
    beta: float = ...,
    alpha: float = ...,
    L: Optional[Any] = ...,
    domain: Any = ...,
    metric: Optional[Any] = ...,
): ...
def navigable_small_world_graph(
    n,
    p: int = ...,
    q: int = ...,
    r: int = ...,
    dim: int = ...,
    seed: Optional[Any] = ...,
): ...
def thresholded_random_geometric_graph(
    n,
    radius,
    theta,
    dim: int = ...,
    pos: Optional[Any] = ...,
    weight: Optional[Any] = ...,
    p: int = ...,
): ...
