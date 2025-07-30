from cache_sim.src.base_cache import BaseCache


class ClockCache(BaseCache):
    def __init__(self, size: int):
        super().__init__(size)
        self.clock = [None] * size  # Circular buffer for entries
        self.refs = [0] * size  # Reference bits
        self.pointer = 0  # Clock hand pointer
        self.index_map = {}  # Map to check address presence and position

    def access(self, address):
        self.total_accesses += 1

        # Hit
        if address in self.index_map:
            idx = self.index_map[address]
            self.refs[idx] = 1  # Mark as recently used
            self.hits += 1
            return True

        # Miss
        self.misses += 1

        # If there's space, insert directly
        if None in self.clock:
            idx = self.clock.index(None)
            self.clock[idx] = address
            self.refs[idx] = 1
            self.index_map[address] = idx
            return False

        # Eviction process
        while True:
            if self.refs[self.pointer] == 0:
                # Evict current
                evicted_addr = self.clock[self.pointer]
                del self.index_map[evicted_addr]
                self.clock[self.pointer] = address
                self.refs[self.pointer] = 1
                self.index_map[address] = self.pointer
                self.evictions += 1
                self.pointer = (self.pointer + 1) % self.size
                return False
            else:
                self.refs[self.pointer] = 0
                self.pointer = (self.pointer + 1) % self.size

    def reset(self):
        self.clock = [None] * self.size
        self.refs = [0] * self.size
        self.pointer = 0
        self.index_map.clear()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.total_accesses = 0
