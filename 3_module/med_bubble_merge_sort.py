import copy
from dataclasses import dataclass
from functools import total_ordering
from typing import List, Optional
from datetime import date, datetime
import time

import os

import requests
import json
from abc import ABC, abstractmethod


class BaseDataUtil(ABC):
    def __init__(self):
        self.json_data = None

    @abstractmethod
    def download_from_url(self, url: str):
        pass

    @abstractmethod
    def save_to_file(self, url: str, filepath: str):
        pass


class DataUtil(BaseDataUtil):

    def download_from_url(self, url: str, is_json: bool = True, is_csv: bool = False):
        """Download data file from URL and store in memory."""
        response = requests.get(url)
        response.raise_for_status()
        if is_json:
            self.json_data = response.json()
        if is_csv:
            raise NotImplementedError("This method must be implemented by subclasses.")

    def save_to_file(self, base_url: str, filepath: str) -> json:
        """Save in-memory data to file, or download if not already loaded."""
        if self.json_data is None:
            print("Data not in memory. Downloading...")
            self.download_from_url(f"{base_url}/{filepath}")

        os.makedirs("target", exist_ok=True)
        filepath = f"target/{filepath}"
        with open(filepath, "w") as f:
            json.dump(self.json_data, f, indent=2)
        return self.json_data


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
        return (self.patient_id, self.name, self.gender, self.date_of_birth) == (
            other.patient_id,
            other.name,
            other.gender,
            other.date_of_birth,
        )

    def __lt__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return (self.name.last_name, self.name.first_name, self.patient_id) < (
            other.name.last_name,
            other.name.first_name,
            other.patient_id,
        )


class EMRSystem(ABC):
    def __init__(self):
        self.records: List[Patient] = []
        self.original_ordered_records: List[Patient] = []

    @abstractmethod
    def add_record(self, patient: Patient) -> "HospitalEMRSystem":
        pass

    @abstractmethod
    def list_records(self) -> List[Patient]:
        pass

    @abstractmethod
    def bubble_sort_records(self, field: str) -> "HospitalEMRSystem":
        pass

    @abstractmethod
    def merge_sort_records(self, field: str) -> "HospitalEMRSystem":
        pass

    @abstractmethod
    def revert(self) -> "HospitalEMRSystem":
        pass

    @abstractmethod
    def load_from_json_file(self, filepath: str) -> List[Patient]:
        pass


class HospitalEMRSystem(EMRSystem):

    @staticmethod
    def _get_sort_key(patient: Patient, field_path: str):
        attributes = field_path.split(".")
        current_value = patient
        for attribute in attributes:
            current_value = getattr(current_value, attribute)
        return current_value

    def add_record(self, patient: Patient) -> "HospitalEMRSystem":
        self.add_records([patient])
        return self

    def add_records(self, patients: List[Patient]) -> "HospitalEMRSystem":
        self.records.extend(patients)
        self.original_ordered_records.extend(patients)
        return self

    def list_records(self, original: bool = False) -> List[Patient]:
        if original:
            return self.original_ordered_records
        return self.records

    def revert(self) -> "HospitalEMRSystem":
        self.records = copy.deepcopy(self.original_ordered_records)
        return self

    def bubble_sort_records(self, field: str) -> "HospitalEMRSystem":
        record_count = len(self.records)

        for pass_num in range(record_count):
            for idx in range(0, record_count - pass_num - 1):
                left_value = self._get_sort_key(self.records[idx], field)
                right_value = self._get_sort_key(self.records[idx + 1], field)
                if left_value > right_value:
                    self.records[idx], self.records[idx + 1] = (
                        self.records[idx + 1],
                        self.records[idx],
                    )
        return self

    def merge_sort_records(self, field: str) -> "HospitalEMRSystem":
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

    @staticmethod
    def json_to_patients(json_data: dict = None) -> List[Patient]:
        """Parse in-memory JSON to Patient objects or load from file."""

        patients = []
        for item in json_data:
            name = Name(**item["name"])
            dob = datetime.fromisoformat(item["date_of_birth"]).date()
            patient = Patient(
                patient_id=item["patient_id"],
                name=name,
                gender=item["gender"],
                date_of_birth=dob,
            )
            patients.append(patient)
        return patients

    def load_from_json_file(self, filepath: str) -> List[Patient]:
        """Load data from file."""
        with open(filepath, "r") as f:
            json_data = json.load(f)
            parsed_data = self.json_to_patients(json_data)
            self.add_records(parsed_data)
            return parsed_data


def load_records(records_path):

    util = DataUtil()
    emr = HospitalEMRSystem()
    base_url = "https://raw.githubusercontent.com/jodth07/algorithm_design_analysis/refs/heads/develop/resources/data"

    if not os.path.exists(f"target/{records_path}"):
        print(f"File target/{records_path} does not exist.")
        json_data = util.download_from_url(f"{base_url}/{records_path}")
        emr.add_records(emr.json_to_patients(json_data))
    else:
        emr.load_from_json_file(f"target/{records_path}")

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


def run_benchmarking(file):
    loaded_emr = load_records(file)

    bubble_time = benchmark_bbs(loaded_emr)
    print(f"Bubble Sort took {bubble_time:.6f} seconds")

    print([p.name.last_name for p in loaded_emr.list_records()][:10])

    loaded_emr.revert()
    print("Revert to original Order for bench marking")
    print([p.name.last_name for p in loaded_emr.list_records()][:10])

    merge_time = benchmark_ms(loaded_emr)
    print(f"Merge Sort took {merge_time:.6f} seconds")
    print([p.name.last_name for p in loaded_emr.list_records()][:10])


if __name__ == "__main__":
    print("\nBenchmarking 50...")
    run_benchmarking("patients_50.json")
    print("\nBenchmarking 100...")
    run_benchmarking("patients_100.json")
