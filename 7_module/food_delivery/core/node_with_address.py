from core.edge_base import Edge
from core.node_base import Node
from core.location import Coordinate, Address
from typing import Set

class NodeWithAddress(Node):
    def __init__(self, name: str, address: Address, coord: Coordinate):
        self._name = name
        self._address = address
        self._coord = coord
        self._neighbors: Set[Node] = set()

    def is_leaf(self) -> bool:
        """Check if the node is a leaf node (no neighbors)."""
        return len(self._neighbors) == 0


    def add_neighbor(self, neighbor: Node):
        self._neighbors.add(neighbor)

    def get_neighbors(self) -> Set[Node]:
        return self._neighbors

    @property
    def coords(self) -> Coordinate:
        return self._coord

    def __str__(self):
        return f"{self._name} ({self._address})"

    @property
    def name(self) -> str:
        return self._name

    def add_edge(self, edge: Edge) -> None:
        self._edges.add(edge)