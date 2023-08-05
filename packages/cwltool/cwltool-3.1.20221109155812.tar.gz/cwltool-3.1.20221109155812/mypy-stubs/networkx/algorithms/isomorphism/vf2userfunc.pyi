# Stubs for networkx.algorithms.isomorphism.vf2userfunc (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

from . import isomorphvf2 as vf2

class GraphMatcher(vf2.GraphMatcher):
    node_match: Any = ...
    edge_match: Any = ...
    G1_adj: Any = ...
    G2_adj: Any = ...
    def __init__(
        self, G1, G2, node_match: Optional[Any] = ..., edge_match: Optional[Any] = ...
    ) -> None: ...
    semantic_feasibility: Any = ...

class DiGraphMatcher(vf2.DiGraphMatcher):
    node_match: Any = ...
    edge_match: Any = ...
    G1_adj: Any = ...
    G2_adj: Any = ...
    def __init__(
        self, G1, G2, node_match: Optional[Any] = ..., edge_match: Optional[Any] = ...
    ) -> None: ...
    def semantic_feasibility(self, G1_node, G2_node): ...

class MultiGraphMatcher(GraphMatcher): ...
class MultiDiGraphMatcher(DiGraphMatcher): ...
