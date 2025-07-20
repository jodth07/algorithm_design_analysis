import unittest
from cache import Cache


class TestCacheFIFO(unittest.TestCase):
    def test_fifo_basic(self):
        cache = Cache(size=3, policy="FIFO")
        accesses = [1, 2, 3, 4]  # will evict 1
        expected_hits = 0

        for addr in accesses:
            hit = cache.access(addr)
            self.assertFalse(hit)

        stats = cache.stats()
        self.assertEqual(stats["Hits"], expected_hits)
        self.assertEqual(stats["Misses"], 4)
        self.assertEqual(stats["Evictions"], 1)

    def test_fifo_with_hit(self):
        cache = Cache(size=3, policy="FIFO")
        trace = [1, 2, 3, 1, 4]  # hit on second 1
        expected_hits = 1

        for addr in trace:
            cache.access(addr)

        stats = cache.stats()
        self.assertEqual(stats["Hits"], expected_hits)
        self.assertEqual(stats["Misses"], 4)
        self.assertEqual(stats["Evictions"], 1)


class TestCacheLRU(unittest.TestCase):
    def test_lru_basic(self):
        cache = Cache(size=2, policy="LRU")
        accesses = [1, 2, 3]  # should evict 1
        cache.access(1)  # miss
        cache.access(2)  # miss
        cache.access(3)  # evict 1

        stats = cache.stats()
        self.assertEqual(stats["Misses"], 3)
        self.assertEqual(stats["Evictions"], 1)
        self.assertEqual(stats["Hits"], 0)

    def test_lru_with_hits(self):
        cache = Cache(size=2, policy="LRU")
        cache.access(1)  # miss
        cache.access(2)  # miss
        cache.access(1)  # hit (1 is most recently used)
        cache.access(3)  # evict 2

        stats = cache.stats()
        self.assertEqual(stats["Hits"], 1)
        self.assertEqual(stats["Misses"], 3)
        self.assertEqual(stats["Evictions"], 1)
        self.assertNotIn(2, cache.cache)  # LRU is evicted

    def test_lru_eviction_order(self):
        cache = Cache(size=2, policy="LRU")
        cache.access(1)  # miss
        cache.access(2)  # miss
        cache.access(1)  # hit
        cache.access(3)  # evict 2

        self.assertNotIn(2, cache.cache)
        self.assertIn(1, cache.cache)
        self.assertIn(3, cache.cache)


class TestEdgeCases(unittest.TestCase):

    def test_zero_size_cache(self):
        cache = Cache(size=0, policy="LRU")
        result = cache.access(1)
        self.assertFalse(result)
        self.assertEqual(cache.stats()["Hits"], 0)
        self.assertEqual(cache.stats()["Misses"], 1)
        self.assertEqual(cache.stats()["Evictions"], 0)

    def test_one_item_cache(self):
        cache = Cache(size=1, policy="FIFO")
        self.assertFalse(cache.access(1))  # miss
        self.assertTrue(cache.access(1))  # hit
        self.assertFalse(cache.access(2))  # miss, evicts 1
        self.assertFalse(cache.access(1))  # miss, 2 was only one in cache

        stats = cache.stats()
        self.assertEqual(stats["Hits"], 1)
        self.assertEqual(stats["Misses"], 3)
        self.assertEqual(stats["Evictions"], 2)

    def test_invalid_policy(self):
        with self.assertRaises(ValueError):
            Cache(size=3, policy="UNKNOWN")

    def test_duplicate_accesses(self):
        cache = Cache(size=2, policy="LRU")
        cache.access(1)  # miss
        cache.access(1)  # hit
        cache.access(1)  # hit

        stats = cache.stats()
        self.assertEqual(stats["Hits"], 2)
        self.assertEqual(stats["Misses"], 1)

    def test_reset_functionality(self):
        cache = Cache(size=2, policy="FIFO")
        cache.access(1)
        cache.access(2)
        cache.access(3)
        self.assertEqual(cache.stats()["Evictions"], 1)

        cache.reset()
        self.assertEqual(cache.stats()["Total Accesses"], 0)
        self.assertEqual(cache.stats()["Hits"], 0)
        self.assertEqual(cache.stats()["Misses"], 0)
        self.assertEqual(cache.stats()["Evictions"], 0)


if __name__ == "__main__":
    unittest.main()
