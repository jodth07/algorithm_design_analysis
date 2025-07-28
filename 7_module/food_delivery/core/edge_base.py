from abc import ABC, abstractmethod


class Edge(ABC):
    @property
    @abstractmethod
    def u_node(self): ...

    @property
    @abstractmethod
    def v_node(self): ...

    @property
    @abstractmethod
    def weight(self) -> float: ...

    @weight.setter
    @abstractmethod
    def weight(self, w: float) -> None: ...
