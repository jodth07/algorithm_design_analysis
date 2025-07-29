from collections import deque, OrderedDict
from base_cache import BaseCache
from metrics import Metrics


class Cache(BaseCache):
    def __init__(self, size, policy="LRU"):
        super().__init__(size)
        self.size = size
        self.policy = policy.upper()
        self.metrics = Metrics()

        if self.policy == "FIFO":
            self.cache = deque()
        elif self.policy == "LRU":
            self.cache = OrderedDict()
        else:
            raise ValueError(f"Unsupported policy: {self.policy}")

    def access(self, address):
        if self.policy == "FIFO":
            return self._access_fifo(address)
        elif self.policy == "LRU":
            return self._access_lru(address)

    def _access_fifo(self, address):
        if address in self.cache:
            self.metrics.record_hit()
            return True
        else:
            self.metrics.record_miss()
            if self.size > 0:
                if len(self.cache) >= self.size:
                    self.cache.popleft()
                    self.metrics.record_eviction()
                self.cache.append(address)
            return False

    def _access_lru(self, address):
        if address in self.cache:
            self.metrics.record_hit()
            self.cache.move_to_end(address)
            return True
        else:
            self.metrics.record_miss()
            if self.size > 0:
                if len(self.cache) >= self.size:
                    self.cache.popitem(last=False)
                    self.metrics.record_eviction()
                self.cache[address] = None
            return False

    def stats(self):
        return self.metrics.summary()

    def reset(self):
        self.metrics.reset()
        if self.policy == "FIFO":
            self.cache = deque()
        elif self.policy == "LRU":
            self.cache = OrderedDict()
