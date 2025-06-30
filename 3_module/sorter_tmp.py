from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from datetime import date
import time

@dataclass
class Name:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

@dataclass
class Patient:
    patient_id: str
    name: Name
    gender: str
    date_of_birth: date


class EMRSystem(ABC):
    def __init__(self):
        self.records: List[Patient] = []
        self.original_ordered_records: List[Patient] = []

    @abstractmethod
    def add_record(self, patient: Patient):
        pass

    @abstractmethod
    def list_records(self) -> List[Patient]:
        pass

    @abstractmethod
    def bubble_sort_records(self, field: str) -> float:
        pass

    @abstractmethod
    def merge_sort_records(self, field: str) -> float:
        pass


class HospitalEMRSystem(EMRSystem):

    @staticmethod
    def _get_sort_key(patient: Patient, field: str):
        # Support nested fields like "name.last_name"
        parts = field.split(".")
        value = patient
        for part in parts:
            value = getattr(value, part)
        return value

    def add_record(self, patient: Patient):
        self.records.append(patient)
        self.original_ordered_records.append(patient)

    def list_records(self) -> List[Patient]:
        return self.records

    def bubble_sort_records(self, field: str) -> float:
        start = time.time()
        n = len(self.records)

        for i in range(n):
            for j in range(0, n - i - 1):
                a = self._get_sort_key(self.records[j], field)
                b = self._get_sort_key(self.records[j + 1], field)
                if a > b:
                    self.records[j], self.records[j + 1] = self.records[j + 1], self.records[j]

        return time.time() - start

    def merge_sort_records(self, field: str) -> float:
        def merge_sort(arr: List[Patient]) -> List[Patient]:
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            return merge(left, right)

        def merge(left: List[Patient], right: List[Patient]) -> List[Patient]:
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                a = self._get_sort_key(left[i], field)
                b = self._get_sort_key(right[j], field)
                if a <= b:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged

        start = time.time()
        self.records = merge_sort(self.records)
        return time.time() - start


if __name__ == "__main__":
    emr = HospitalEMRSystem()

    # Add sample records (unsorted)
    emr.add_record(Patient("P001", Name("Alice", "Zane", "Davis"), "Female", date(1990, 4, 2)))
    emr.add_record(Patient("P002", Name("Bob", "Young"), "Female", date(1985, 5, 15)))
    emr.add_record(Patient("P003", Name("Charlie", "Smith"), "Female", date(1975, 8, 24)))
    emr.add_record(Patient("P004", Name( "Diana", "Brown"), "Female", date(1992, 11, 1)))
    emr.add_record(Patient("P005", Name("Evan", "Anderson"), "Female", date(2000, 2, 10)))

    print("Original:")
    for p in emr.list_records():
        print(p.name.last_name)

    # Bubble sort benchmark
    bubble_time = emr.bubble_sort_records("name.last_name")
    print("\nAfter Bubble Sort:")
    for p in emr.list_records():
        print(p.name.last_name)
    print(f"Bubble Sort took {bubble_time:.6f} seconds")

    # Re-shuffle for merge sort benchmark
    emr.records.reverse()

    merge_time = emr.merge_sort_records("name.last_name")
    print("\nAfter Merge Sort:")
    for p in emr.list_records():
        print(p.name.last_name)
    print(f"Merge Sort took {merge_time:.6f} seconds")
