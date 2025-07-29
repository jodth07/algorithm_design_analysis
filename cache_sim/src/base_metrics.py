from abc import ABC, abstractmethod


class BaseMetrics(ABC):
    @abstractmethod
    def record_hit(self):
        pass

    @abstractmethod
    def record_miss(self):
        pass

    @abstractmethod
    def record_eviction(self):
        pass

    @abstractmethod
    def summary(self) -> dict:
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def set_memory_used(self, bytes_used):
        pass
