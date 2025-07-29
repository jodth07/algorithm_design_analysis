from abc import ABC, abstractmethod
from core.location import Coordinate, Address
from core.edge_base import Edge
from typing import Set


class Node(ABC):
    _address: Address = None
    _neighbors: Set["Node"] = []
    _coord: Coordinate = None
    _edges: Set[Edge] = set()

    def is_leaf(self) -> bool:
        """Check if the node is a leaf node (no neighbors)."""
        ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def coords(self) -> Coordinate: ...

    @abstractmethod
    def add_neighbor(self, neighbor: "Node") -> None: ...

    @abstractmethod
    def get_neighbors(self) -> Set["Node"]: ...

    @property
    def edges(self) -> Set[Edge]:
        return self._edges

    @abstractmethod
    def add_edge(self, edge: Edge) -> None: ...
