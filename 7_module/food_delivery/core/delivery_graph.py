from core.base_graph import AbstractGraph
from core.node_base import Node
from core.edge_with_traffic import EdgeWithTraffic

class DeliveryGraph(AbstractGraph):
    def __init__(self):
        self.nodes = {}

    def add_node(self, node: Node) -> 'DeliveryGraph':
        if node.name not in self.nodes:
            self.nodes[node.name] = node
        return self

    def add_edge(self, u_node: Node, v_node: Node):
        edge = EdgeWithTraffic(u_node, v_node)
        rev_edge = EdgeWithTraffic(v_node, u_node)

        u_node.add_edge(edge)
        u_node.add_neighbor(v_node)

        v_node.add_edge(rev_edge)
        v_node.add_neighbor(u_node)

    def get_all_edges(self):
        seen = set()
        edges = []
        for node in self.nodes.values():
            for edge in node.edges:
                key = tuple(sorted([edge.u_node.name, edge.v_node.name]))
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)
        return edges

    def run_algorithm(self, algorithm, start, end):
        return algorithm.run(self, start, end)

    def get_neighbors(self, node_name):
        node = self.nodes.get(node_name)
        if not node or node.is_leaf():
            return []

        neighbors = []
        for edge in node.edges:
            if edge.u_node.name == node_name:
                neighbors.append((edge.v_node.name, edge.weight))
        return neighbors

    def get_node(self, node_name):
        return self.nodes.get(node_name)
