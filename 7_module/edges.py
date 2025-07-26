from abc import ABC, abstractmethod

class AbstractEdge(ABC):
    @abstractmethod
    def get_weight(self):
        pass


class Edge(AbstractEdge):
    def __init__(self, from_node, to_node, base_weight):
        self.from_node = from_node
        self.to_node = to_node
        self.base_weight = base_weight
        self.weight = base_weight

    def get_weight(self):
        return self.weight

    def __repr__(self):
        return f"Edge({self.from_node.name} -> {self.to_node.name}, {self.weight})"
