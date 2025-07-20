import random
from typing import List, Union
import numpy as np  # You'll need numpy installed
from base_parser import BaseParser


class FileParser(BaseParser):
    def __init__(self, filepath: str, cast_to_int: bool = True):
        self.filepath = filepath
        self.cast_to_int = cast_to_int

    def load(self) -> List[Union[int, str]]:
        addresses = []
        with open(self.filepath, "r") as f:
            for line in f:
                addr = line.strip()
                if addr:
                    addresses.append(int(addr) if self.cast_to_int else addr)
        return addresses


class SyntheticParser(BaseParser):
    def __init__(
        self, num_accesses: int = 100, address_space: int = 50, seed: int = None
    ):
        self.num_accesses = num_accesses
        self.address_space = address_space
        self.rng = random.Random(seed)

    def load(self) -> List[int]:
        return [
            self.rng.randint(0, self.address_space - 1)
            for _ in range(self.num_accesses)
        ]


class ZipfianParser(BaseParser):
    def __init__(
        self,
        num_accesses: int = 100,
        address_space: int = 50,
        skew: float = 1.2,
        seed: int = None,
    ):
        self.num_accesses = num_accesses
        self.address_space = address_space
        self.skew = skew
        self.rng = np.random.default_rng(seed)

    def load(self) -> List[int]:
        # Generate Zipf-distributed integers (1, 2, 3, ...)
        raw_zipf = self.rng.zipf(self.skew, self.num_accesses)

        # Map into the address space [0, address_space - 1]
        mapped = [(x - 1) % self.address_space for x in raw_zipf]
        return mapped
