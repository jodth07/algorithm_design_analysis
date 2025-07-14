from base_metrics import BaseMetrics


class Metrics(BaseMetrics):
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    def record_eviction(self):
        self.evictions += 1

    def total_accesses(self):
        return self.hits + self.misses

    def hit_rate(self):
        total = self.total_accesses()
        return self.hits / total if total > 0 else 0.0

    def miss_rate(self):
        total = self.total_accesses()
        return self.misses / total if total > 0 else 0.0

    def eviction_rate(self):
        total = self.total_accesses()
        return self.evictions / total if total > 0 else 0.0

    def summary(self) -> dict:
        return {
            "Total Accesses": self.total_accesses(),
            "Hits": self.hits,
            "Misses": self.misses,
            "Evictions": self.evictions,
            "Hit Rate": round(self.hit_rate(), 4),
            "Miss Rate": round(self.miss_rate(), 4),
            "Eviction Rate": round(self.eviction_rate(), 4),
        }

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.summary().items())

    def reset(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
