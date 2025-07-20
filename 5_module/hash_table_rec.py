from abc import ABC, abstractmethod
from typing import Any, Optional, List, Tuple, Hashable
import numpy as np


class AbstractHashTable(ABC):
    def __init__(self, size: int = 10) -> None:
        self.table = None
        self.size: int = size

    @abstractmethod
    def _hash_index(self, key: str) -> int:
        pass

    @abstractmethod
    def put(self, key: str, value: Any) -> bool:
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def remove(self, key: str) -> bool:
        pass

    @abstractmethod
    def recommend_by_hash(self, user_hash: str) -> Optional[Any]:
        pass

    @staticmethod
    def binary_hash(embedding: np.ndarray, projection_matrix: np.ndarray) -> str:
        projection = np.dot(embedding, projection_matrix)
        return ''.join('1' if val >= 0 else '0' for val in projection)

    @staticmethod
    def hamming_distance(hash1: str, hash2: str) -> int:
        return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))


class HashTable(AbstractHashTable):
    def __init__(self, size: int = 10):
        super().__init__(size)
        self.size = size
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(size)]

    def _hash_index(self, key: str) -> int:
        return hash(key) % self.size

    def put(self, key: str, value: Any) -> bool:
        index = self._hash_index(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return True
        self.table[index].append((key, value))
        return True

    def get(self, key: str) -> Optional[Any]:
        index = self._hash_index(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def remove(self, key: str) -> bool:
        index = self._hash_index(key)
        for i, (k, _) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False

    def recommend_by_hash(self, user_hash: str) -> Optional[Any]:
        closest_match = None
        smallest_distance = float('inf')
        for bucket in self.table:
            for content_hash, content in bucket:
                distance = self.hamming_distance(user_hash, content_hash)
                if distance < smallest_distance:
                    smallest_distance = distance
                    closest_match = content
        return closest_match


if __name__ == "__main__":
    np.random.seed(42)
    embedding_dim = 8
    hash_length = 16
    projection_matrix = np.random.randn(embedding_dim, hash_length)

    content_embeddings = {
        "video_101": np.random.rand(embedding_dim),
        "video_202": np.random.rand(embedding_dim),
        "video_303": np.random.rand(embedding_dim),
        "video_404": np.random.rand(embedding_dim),
    }

    ht = HashTable(size=20)
    for content_id, emb in content_embeddings.items():
        content_hash = ht.binary_hash(emb, projection_matrix)
        ht.put(content_hash, content_id)

    print("----- User Recommendations -----")
    for i in range(4):
        user_embedding = np.random.rand(embedding_dim)
        user_hash = ht.binary_hash(user_embedding, projection_matrix)
        print(f"\nUser {i + 1} binary hash: {user_hash}")

        recommendation = ht.get(user_hash)
        if recommendation:
            print(f"Exact match recommendation: {recommendation}")
        else:
            fallback = ht.recommend_by_hash(user_hash)
            print(f"Fallback recommendation (nearest match): {fallback}")
