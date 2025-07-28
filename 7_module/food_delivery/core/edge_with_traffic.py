from core.edge_base import Edge
from core.node_with_address import Node
from core.traffic import get_travel_time_tomtom


class EdgeWithTraffic(Edge):
    def __init__(self, u_node: Node, v_node: Node):
        self._u_node = u_node
        self._v_node = v_node
        self._weight = get_travel_time_tomtom(u_node.coords, v_node.coords)

    @property
    def u_node(self) -> Node:
        return self._u_node

    @property
    def v_node(self) -> Node:
        return self._v_node

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w
