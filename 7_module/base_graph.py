from abc import ABC, abstractmethod
from nodes import Node
from edges import Edge


class AbstractGraph(ABC):
    @abstractmethod
    def add_edge(self, from_name, to_name, base_weight, from_coords, to_coords):
        pass

    @abstractmethod
    def run_algorithm(self, algorithm, start, end):
        pass


class DeliveryGraph(AbstractGraph):
    def __init__(self):
        self.nodes = {}

    def add_node(self, name, lat, lon):
        if name not in self.nodes:
            self.nodes[name] = Node(name, lat, lon)
        return self.nodes[name]

    def add_edge(self, from_name, to_name, base_weight, from_coords, to_coords):
        from_node = self.add_node(from_name, *from_coords)
        to_node = self.add_node(to_name, *to_coords)

        edge = Edge(from_node, to_node, base_weight)
        rev_edge = Edge(to_node, from_node, base_weight)

        from_node.edges.append(edge)
        to_node.edges.append(rev_edge)

    def get_all_edges(self):
        seen = set()
        edges = []
        for node in self.nodes.values():
            for edge in node.edges:
                key = tuple(sorted([edge.from_node.name, edge.to_node.name]))
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)
        return edges

    def run_algorithm(self, algorithm, start, end):
        return algorithm.run(self, start, end)

    def get_neighbors(self, node_name):
        node = self.nodes.get(node_name)
        if not node:
            return []
        return [(e.to_node.name, e.get_weight()) for e in node.edges]

    def get_node(self, name):
        return self.nodes.get(name)
