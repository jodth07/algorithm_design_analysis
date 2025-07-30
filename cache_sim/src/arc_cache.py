from collections import deque
from cache_sim.src.base_cache import BaseCache


class ARCCache(BaseCache):
    def __init__(self, size: int):
        super().__init__(size)
        self.T1 = deque()
        self.T2 = deque()
        self.B1 = deque()
        self.B2 = deque()
        self.p = 0  # Adaptive parameter

    def access(self, address):
        self.total_accesses += 1

        if address in self.T1:
            self.T1.remove(address)
            self.T2.appendleft(address)
            self.hits += 1
            return True

        if address in self.T2:
            self.T2.remove(address)
            self.T2.appendleft(address)
            self.hits += 1
            return True

        self.misses += 1

        # Case 1: Address in B1 (recent eviction)
        if address in self.B1:
            self._adjust_p(
                min(len(self.B2), max(1, len(self.B1) // max(1, len(self.B2))))
            )
            self._replace(address)
            self.B1.remove(address)
            self.T2.appendleft(address)
            return False

        # Case 2: Address in B2 (frequent eviction)
        if address in self.B2:
            self._adjust_p(
                -min(len(self.B1), max(1, len(self.B2) // max(1, len(self.B1))))
            )
            self._replace(address)
            self.B2.remove(address)
            self.T2.appendleft(address)
            return False

        # Case 3: Address is new
        if len(self.T1) + len(self.B1) == self.size:
            if len(self.T1) < self.size:
                self.B1.pop()
                self._replace(address)
            else:
                removed = self.T1.pop()
                self.B1.appendleft(removed)
                self.evictions += 1
        elif len(self.T1) + len(self.T2) + len(self.B1) + len(self.B2) >= self.size:
            if (
                len(self.T1) + len(self.T2) + len(self.B1) + len(self.B2)
                >= 2 * self.size
            ):

                if len(self.B2) > 0:
                    self.B2.pop()
            self._replace(address)

        self.T1.appendleft(address)
        return False

    def _adjust_p(self, delta):
        self.p = min(self.size, max(0, self.p + delta))

    def _replace(self, address):
        if len(self.T1) > 0 and (
            len(self.T1) > self.p or (address in self.B2 and len(self.T1) == self.p)
        ):
            removed = self.T1.pop()
            self.B1.appendleft(removed)
            self.evictions += 1
        else:
            if len(self.T2) > 0:
                removed = self.T2.pop()
                self.B2.appendleft(removed)
                self.evictions += 1

    def reset(self):
        self.T1.clear()
        self.T2.clear()
        self.B1.clear()
        self.B2.clear()
        self.p = 0
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.total_accesses = 0
