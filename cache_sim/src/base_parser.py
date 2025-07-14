from abc import ABC, abstractmethod
from typing import List, Union


class BaseParser(ABC):
    @abstractmethod
    def load(self) -> List[Union[str, int]]:
        """
        Loads and returns a list of memory addresses from the source.
        """
        pass
