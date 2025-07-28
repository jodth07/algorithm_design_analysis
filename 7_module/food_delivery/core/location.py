from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float


@dataclass(frozen=True)
class Address:
    street: str
    city: str
    state: str
    zipcode: int
    country: str = "USA"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zipcode}"

    def __repr__(self):
        return f"{self.__str__()}"
