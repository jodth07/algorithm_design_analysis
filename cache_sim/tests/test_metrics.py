import unittest
from ..src.metrics import Metrics


class TestSimpleMetrics(unittest.TestCase):

    def test_tracking(self):
        m = Metrics()
        for _ in range(3):
            m.record_hit()
        for _ in range(2):
            m.record_miss()
        for _ in range(1):
            m.record_eviction()

        self.assertEqual(m.total_accesses(), 5)
        self.assertEqual(m.hit_rate(), 3 / 5)
        self.assertEqual(m.miss_rate(), 2 / 5)
        self.assertEqual(m.eviction_rate(), 1 / 5)

    def test_summary_output(self):
        m = Metrics()
        m.record_hit()
        m.record_miss()
        m.record_eviction()
        summary = m.summary()
        self.assertEqual(summary["Hits"], 1)
        self.assertEqual(summary["Misses"], 1)
        self.assertEqual(summary["Evictions"], 1)

    def test_reset(self):
        m = Metrics()
        m.record_hit()
        m.record_miss()
        m.record_eviction()
        m.reset()
        self.assertEqual(m.total_accesses(), 0)


if __name__ == "__main__":
    unittest.main()
