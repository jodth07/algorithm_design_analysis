import unittest
import os
from ..src.parser import FileParser, SyntheticParser, ZipfianParser


class TestFileParser(unittest.TestCase):
    def setUp(self):
        import os

        self.test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "traces", "test_trace.txt"
        )
        with open(self.test_file, "w") as f:
            f.write("\n".join(["10", "20", "30", "10", "40"]))

    def tearDown(self):
        os.remove(self.test_file)

    def test_file_parser_int(self):
        parser = FileParser(self.test_file, cast_to_int=True)
        result = parser.load()
        expected = [10, 20, 30, 10, 40]
        self.assertEqual(result, expected)
        self.assertTrue(all(isinstance(x, int) for x in result))

    def test_file_parser_str(self):
        parser = FileParser(self.test_file, cast_to_int=False)
        result = parser.load()
        expected = ["10", "20", "30", "10", "40"]
        self.assertEqual(result, expected)
        self.assertTrue(all(isinstance(x, str) for x in result))


class TestSyntheticParser(unittest.TestCase):
    def test_synthetic_parser_length(self):
        parser = SyntheticParser(num_accesses=200, address_space=10, seed=42)
        result = parser.load()
        self.assertEqual(len(result), 200)

    def test_synthetic_parser_range(self):
        parser = SyntheticParser(num_accesses=100, address_space=5, seed=123)
        result = parser.load()
        self.assertTrue(all(0 <= x < 5 for x in result))

    def test_synthetic_parser_repeatable(self):
        parser1 = SyntheticParser(num_accesses=50, address_space=10, seed=99)
        parser2 = SyntheticParser(num_accesses=50, address_space=10, seed=99)
        self.assertEqual(parser1.load(), parser2.load())


class TestZipfianParser(unittest.TestCase):

    def test_zipfian_length(self):
        parser = ZipfianParser(num_accesses=100, address_space=50, skew=1.2, seed=123)
        trace = parser.load()
        self.assertEqual(len(trace), 100)

    def test_zipfian_range(self):
        parser = ZipfianParser(num_accesses=100, address_space=20, skew=1.2, seed=42)
        trace = parser.load()
        self.assertTrue(all(0 <= x < 20 for x in trace))

    def test_zipfian_repeatable(self):
        p1 = ZipfianParser(num_accesses=50, address_space=10, skew=1.2, seed=99)
        p2 = ZipfianParser(num_accesses=50, address_space=10, skew=1.2, seed=99)
        self.assertEqual(p1.load(), p2.load())


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
