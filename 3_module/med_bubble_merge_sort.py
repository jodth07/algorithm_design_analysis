import copy
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import total_ordering
from typing import List, Optional
from datetime import date
import time

from data_util import DataUtil

@dataclass
class Name:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

@total_ordering
@dataclass
class Patient:
    patient_id: str
    name: Name
    gender: str
    date_of_birth: date

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return (self.patient_id, self.name, self.gender, self.date_of_birth) == \
               (other.patient_id, other.name, other.gender, other.date_of_birth)

    def __lt__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        # Default sort by last name, then first name, then patient_id
        return ((self.name.last_name, self.name.first_name, self.patient_id) <
                (other.name.last_name, other.name.first_name, other.patient_id))

class EMRSystem(ABC):
    def __init__(self):
        self.records: List[Patient] = []
        self.original_ordered_records: List[Patient] = []

    @abstractmethod
    def add_record(self, patient: Patient) -> 'HospitalEMRSystem':
        pass

    @abstractmethod
    def list_records(self) -> List[Patient]:
        pass

    @abstractmethod
    def bubble_sort_records(self, field: str) -> 'HospitalEMRSystem':
        pass

    @abstractmethod
    def merge_sort_records(self, field: str) -> 'HospitalEMRSystem':
        pass

    @abstractmethod
    def revert(self) -> 'HospitalEMRSystem':
        pass


class HospitalEMRSystem(EMRSystem):

    @staticmethod
    def _get_sort_key(patient: Patient, field: str) -> Patient:
        parts = field.split(".")
        value = patient
        for part in parts:
            value = getattr(value, part)
        return value

    def add_record(self, patient: Patient) -> 'HospitalEMRSystem':
        self.add_records([patient])
        return self

    def add_records(self, patients: List[Patient]) -> 'HospitalEMRSystem':
        self.records.extend(patients)
        self.original_ordered_records.extend(patients)
        return self

    def list_records(self, original: bool = False) -> List[Patient]:
        if original:
            return self.original_ordered_records
        return self.records

    def revert(self) -> 'HospitalEMRSystem':
        self.records = copy.deepcopy(self.original_ordered_records)
        return self


    def bubble_sort_records(self, field: str) -> 'HospitalEMRSystem':
        n = len(self.records)

        for i in range(n):
            for j in range(0, n - i - 1):
                a = self._get_sort_key(self.records[j], field)
                b = self._get_sort_key(self.records[j + 1], field)
                if a > b:
                    self.records[j], self.records[j + 1] = self.records[j + 1], self.records[j]

        return self

    def merge_sort_records(self, field: str) -> 'HospitalEMRSystem':
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
        self.records = merge_sort(self.records)
        return self


def load_records(records_path):
    os.makedirs("target", exist_ok=True)
    util = DataUtil()
    loaded_data = util.load_from_file(f"target/{records_path}")
    print(len(loaded_data))

    emr = HospitalEMRSystem()
    emr.add_records(loaded_data)

    print("Original:")
    print([p.name.last_name for p in emr.list_records()][:10])
    return emr

def benchmark_bbs(emr) -> float:
    print("\nBubble Sort: Starting ...")
    start_time = time.perf_counter()
    emr.bubble_sort_records("name.last_name")
    end_time = time.perf_counter()
    print(f"Bubble Sort start time:{start_time}")
    print(f"Bubble Sort end time:{end_time}")
    return end_time - start_time

def benchmark_ms(emr) -> float:
    print("\nMerge Sort Starting ...")
    start_time = time.perf_counter()
    emr.merge_sort_records("name.last_name")
    end_time = time.perf_counter()
    print(f"Merge Sort start time:{start_time}")
    print(f"Merge Sort end time:{end_time}")
    return end_time - start_time

if __name__ == "__main__":
    loaded_emr = load_records("patients_50.json")

    # Bubble sort benchmark
    bubble_time = benchmark_bbs(loaded_emr)
    print(f"Bubble Sort took {bubble_time:.6f} seconds")
    print([p.name.last_name for p in loaded_emr.list_records()][:10])

    # Re-shuffle for merge sort benchmark
    loaded_emr.revert()
    print("Revert to original Order for bench marking")
    print([p.name.last_name for p in loaded_emr.list_records()][:10])

    merge_time = benchmark_ms(loaded_emr)
    print(f"Merge Sort took {merge_time:.6f} seconds")
    print([p.name.last_name for p in loaded_emr.list_records()][:10])
