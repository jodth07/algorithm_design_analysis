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
