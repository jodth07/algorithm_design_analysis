from abc import ABC, abstractmethod
from core.node_base import Node

class AbstractGraph(ABC):
    @abstractmethod
    def add_edge(self, from_node: Node, to_node: Node):
        pass

    @abstractmethod
    def run_algorithm(self, algorithm, start, end):
        pass
