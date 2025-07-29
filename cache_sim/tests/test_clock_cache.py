import unittest
from cache.clock_cache import ClockCache  # Adjust import path as needed


class TestClockCache(unittest.TestCase):
    def test_clock_basic(self):
        cache = ClockCache(size=3)
        # Misses
        self.assertFalse(cache.access(1))
        self.assertFalse(cache.access(2))
        self.assertFalse(cache.access(3))

        # Hits
        self.assertTrue(cache.access(1))
        self.assertTrue(cache.access(2))

        # Causes eviction
        self.assertFalse(cache.access(4))  # One of [3] gets evicted
        self.assertEqual(cache.evictions, 1)

    def test_clock_reference_bit_reset(self):
        cache = ClockCache(size=2)
        cache.access(1)  # Miss
        cache.access(2)  # Miss
        cache.access(1)  # Hit, sets ref bit
        cache.access(3)  # Evict 2 (if 1's ref bit protects it)
        self.assertTrue(1 in cache.index_map)
        self.assertTrue(3 in cache.index_map)
        self.assertEqual(cache.evictions, 1)

    def test_clock_reset(self):
        cache = ClockCache(size=2)
        cache.access(1)
        cache.access(2)
        cache.access(3)
        self.assertGreater(cache.total_accesses, 0)

        cache.reset()
        self.assertEqual(cache.total_accesses, 0)
        self.assertEqual(cache.hits, 0)
        self.assertEqual(cache.misses, 0)
        self.assertEqual(cache.evictions, 0)
        self.assertEqual(len(cache.index_map), 0)

    def test_clock_overflow(self):
        cache = ClockCache(size=1)
        cache.access(1)
        cache.access(2)
        cache.access(3)
        self.assertEqual(cache.evictions, 2)
        self.assertEqual(len(cache.index_map), 1)

    def test_clock_repeat_hit(self):
        cache = ClockCache(size=2)
        cache.access(1)
        cache.access(2)
        self.assertTrue(cache.access(1))
        self.assertTrue(cache.access(2))
        self.assertEqual(cache.hits, 2)
        self.assertEqual(cache.evictions, 0)


if __name__ == "__main__":
    unittest.main()
