import requests
import json
from typing import Optional, List
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass

from numpy.f2py.auxfuncs import throw_error


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
    date_of_birth: datetime.date


class BaseDataUtil(ABC):
    @abstractmethod
    def download_to_memory(self, url: str):
        pass

    @abstractmethod
    def save_to_file_if_loaded_or_download(self, url: str, filepath: str):
        pass

    @abstractmethod
    def parse_to_objects(self, filepath: str) -> List[Patient]:
        pass


class DataUtil(BaseDataUtil):
    def __init__(self):
        self._json_data = None  # Holds the in-memory JSON data

    def download_to_memory(self, url: str):
        """Download JSON from URL and store in memory."""
        response = requests.get(url)
        response.raise_for_status()
        self._json_data = response.json()

    def save_to_file_if_loaded_or_download(self, url: str, filepath: str):
        """Save in-memory data to file, or download if not already loaded."""
        if self._json_data is None:
            print("Data not in memory. Downloading...")
            self.download_to_memory(url)
        with open(filepath, "w") as f:
            json.dump(self._json_data, f, indent=2)

    def parse_to_objects(
        self, filepath: Optional[str] = None, url: Optional[str] = None
    ) -> List[Patient]:
        """Parse in-memory JSON to Patient objects or load from file."""
        if self._json_data is None:
            print("Data not in memory. Loading from file...")

        patients = []
        for item in self._json_data:
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

    def load_from_file(self, filepath: str) -> List[Patient]:
        """Load data from file."""
        with open(filepath, "r") as f:
            self._json_data = json.load(f)
        return self.parse_to_objects(self._json_data)
