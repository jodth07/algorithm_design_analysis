from abc import ABC, abstractmethod

class AbstractNode(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_coords(self):
        pass


class Node(AbstractNode):
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.edges = []

    def get_name(self):
        return self.name

    def get_coords(self):
        return (self.latitude, self.longitude)

    def __repr__(self):
        return f"Node({self.name})"
