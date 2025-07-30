from abc import ABC, abstractmethod
from typing import Union


class BaseCache(ABC):
    def __init__(self, size: int):
        self.size = size
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.total_accesses = 0

    @abstractmethod
    def access(self, address: Union[int, str]) -> bool:
        """
        Handle access to a memory address.
        Returns True for hit, False for miss.
        """
        pass

    def stats(self) -> dict:
        return {
            "Total Accesses": self.total_accesses,
            "Hits": self.hits,
            "Misses": self.misses,
            "Evictions": self.evictions,
            "Hit Rate": (
                round(self.hits / self.total_accesses, 4)
                if self.total_accesses
                else 0.0
            ),
            "Miss Rate": (
                round(self.misses / self.total_accesses, 4)
                if self.total_accesses
                else 0.0
            ),
            "Eviction Rate": (
                round(self.evictions / self.total_accesses, 4)
                if self.total_accesses
                else 0.0
            ),
        }

    @abstractmethod
    def reset(self):
        """Reset the cache and stats."""
        pass
