import pprint
from dataclasses import dataclass

from abc import ABC, abstractmethod


class MarketplaceItemsInterface(ABC):
    @abstractmethod
    def __init__(self, items: list[dict] | list["MarketplaceItem"]):
        """
        Initialize MarketplaceItems from a list of dictionaries or MarketplaceItem objects.

        :param items: A list of dictionaries or MarketplaceItem objects.
        """
        pass

    @abstractmethod
    def available_items(self) -> list["MarketplaceItem"]:
        """Return a list of items that are available."""
        pass

    @abstractmethod
    def find_one_by_name(self, name: str) -> list["MarketplaceItem"]:
        """
        Find a single item by name

        :param name: The name of the item to search for.
        :return: A list of MarketplaceItem objects that match the name.
        """
        pass

    @abstractmethod
    def fuzzy_find_by_name(self, name: str) -> list["MarketplaceItem"]:
        """
        Find items by name if substrings are found in name

        :param name: The name of the item to search for.
        :return: A list of MarketplaceItem objects that match the name.
        """
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> list["MarketplaceItem"]:
        """
        Find items by name

        :param name: The name of the item to search for.
        :return: A list of MarketplaceItem objects that match the name.
        """
        pass

    @abstractmethod
    def total_in_stock_quantity(self) -> int:
        """Calculate the total quantity of items in stock."""
        pass

    @abstractmethod
    def filter_by(self, key: str, value: str | int) -> "MarketplaceItems":
        """
        Filter marketplace items by a specific key and value.

        :param key: The attribute to filter by (e.g., 'color', 'storage_gb').
        :param value: The value to match against the specified key.
        :return: A list of MarketplaceItem objects that match the filter criteria.
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """return the number of distinct items in the marketplace catalogs"""
        pass

    @abstractmethod
    def __iter__(self):
        """Make MarketplaceItems iterable."""
        pass


@dataclass(frozen=False)
class MarketplaceItem:
    id: int
    name: str
    color: str
    storage_gb: int
    condition: str
    price: float
    is_in_stock: bool
    is_available: bool
    in_stock_quantity: int

    def __repr__(self):
        return f"MarketplaceItem(name={self.name}, color={self.color}, storage_gb={self.storage_gb}, condition={self.condition}, price={self.price})"


class MarketplaceItems(MarketplaceItemsInterface):
    items: list[MarketplaceItem]

    def __init__(self, items: list[dict] | list[MarketplaceItem]):
        """
        Initialize MarketplaceItems from a list of dictionaries or MarketplaceItem objects.

        :param items: A list of dictionaries or MarketplaceItem objects.
        """
        if all(isinstance(item, dict) for item in items):
            object_items = [MarketplaceItem(**item) for item in items]
        elif all(isinstance(item, MarketplaceItem) for item in items):
            object_items = items
        else:
            raise TypeError(
                "Items must be a list of dictionaries or MarketplaceItem objects."
            )

        object.__setattr__(self, "items", object_items)

    def available_items(self) -> list["MarketplaceItem"]:
        """Return a list of items that are available."""
        return [item for item in self.items if item.is_available]

    def find_one_by_name(self, name: str) -> list["MarketplaceItem"]:
        """
        Find a single item by name

        :param name: The name of the item to search for.
        :return: A list of MarketplaceItem objects that match the name.
        """
        return [item for item in self.items if item.name.lower() == name.lower()]

    def fuzzy_find_by_name(self, name: str) -> list["MarketplaceItem"]:
        """
        Find items by name if substrings are found in name

        :param name: The name of the item to search for.
        :return: A list of MarketplaceItem objects that match the name.
        """
        return [
            item
            for item in self.items
            if all(letter in item.name.lower() for letter in set(name.lower()))
        ]

    def find_by_name(self, name: str) -> list[MarketplaceItem]:
        """
        Find items by name

        :param name: The name of the item to search for.
        :return: A list of MarketplaceItem objects that match the name.
        """
        return [item for item in self.items if item.name.lower() == name.lower()]

    def total_in_stock_quantity(self) -> int:
        """Calculate the total quantity of items in stock."""
        return sum(item.in_stock_quantity for item in self.items if item.is_in_stock)

    def filter_by(self, key: str, value: str | int) -> "MarketplaceItems":
        """
        Filter marketplace items by a specific key and value.

        :param key: The attribute to filter by (e.g., 'color', 'storage_gb').
        :param value: The value to match against the specified key.
        :return: A list of MarketplaceItem objects that match the filter criteria.
        """
        range_filters = ["storage_gb", "price"]
        exact_filter_keys = ["color", "condition"]
        all_filter_keys = range_filters + exact_filter_keys
        if key not in all_filter_keys:
            raise ValueError(
                f"Invalid key: {key}. Available keys are: {', '.join(all_filter_keys)}"
            )

        return MarketplaceItems(
            [item for item in self.available_items() if getattr(item, key) == value]
        )

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        """Make MarketplaceItems iterable."""
        return iter(self.items)


if __name__ == "__main__":
    market_place = [
        {
            "id": 1,
            "name": "iPhone 16 Pro Max",
            "color": "Black",
            "storage_gb": 1000,
            "condition": "New",
            "price": 1599.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 50,
        },
        {
            "id": 2,
            "name": "iPhone 16 Pro Max",
            "color": "Black",
            "storage_gb": 512,
            "condition": "New",
            "price": 1399.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 75,
        },
        {
            "id": 3,
            "name": "iPhone 16 Pro",
            "color": "White Titanium",
            "storage_gb": 256,
            "condition": "New",
            "price": 1099.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 120,
        },
        {
            "id": 4,
            "name": "iPhone 16 Pro",
            "color": "Blue Titanium",
            "storage_gb": 128,
            "condition": "New",
            "price": 999.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 100,
        },
        {
            "id": 5,
            "name": "iPhone 16 Plus",
            "color": "Ultramarine",
            "storage_gb": 256,
            "condition": "New",
            "price": 899.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 90,
        },
        {
            "id": 6,
            "name": "iPhone 16",
            "color": "Teal",
            "storage_gb": 128,
            "condition": "New",
            "price": 799.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 130,
        },
        {
            "id": 7,
            "name": "iPhone 16e",
            "color": "Black",
            "storage_gb": 64,
            "condition": "New",
            "price": 429.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 80,
        },
        {
            "id": 8,
            "name": "iPhone 15 Pro Max",
            "color": "Black",
            "storage_gb": 1000,
            "condition": "New",
            "price": 1399.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 40,
        },
        {
            "id": 9,
            "name": "iPhone 15 Pro Max",
            "color": "White Titanium",
            "storage_gb": 512,
            "condition": "New",
            "price": 1299.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 60,
        },
        {
            "id": 10,
            "name": "iPhone 15 Pro",
            "color": "Black",
            "storage_gb": 256,
            "condition": "New",
            "price": 999.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 100,
        },
        {
            "id": 11,
            "name": "iPhone 15",
            "color": "Pink",
            "storage_gb": 128,
            "condition": "New",
            "price": 799.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 110,
        },
        {
            "id": 12,
            "name": "iPhone 15 Plus",
            "color": "Blue",
            "storage_gb": 256,
            "condition": "New",
            "price": 899.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 70,
        },
        {
            "id": 13,
            "name": "iPhone 14 Pro Max",
            "color": "Deep Purple",
            "storage_gb": 512,
            "condition": "Used - Excellent",
            "price": 650.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 15,
        },
        {
            "id": 14,
            "name": "iPhone 14",
            "color": "Midnight",
            "storage_gb": 128,
            "condition": "Used - Good",
            "price": 350.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 25,
        },
        {
            "id": 15,
            "name": "iPhone SE (3rd Gen)",
            "color": "Starlight",
            "storage_gb": 64,
            "condition": "New",
            "price": 329.99,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 50,
        },
        {
            "id": 16,
            "name": "iPhone 13 Pro Max",
            "color": "Sierra Blue",
            "storage_gb": 256,
            "condition": "Used - Excellent",
            "price": 550.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 10,
        },
        {
            "id": 17,
            "name": "iPhone 13 mini",
            "color": "Pink",
            "storage_gb": 128,
            "condition": "Used - Good",
            "price": 220.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 18,
        },
        {
            "id": 18,
            "name": "iPhone 12 Pro",
            "color": "Pacific Blue",
            "storage_gb": 256,
            "condition": "Used - Good",
            "price": 400.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 12,
        },
        {
            "id": 19,
            "name": "iPhone 12",
            "color": "Green",
            "storage_gb": 64,
            "condition": "Used - Fair",
            "price": 250.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 30,
        },
        {
            "id": 20,
            "name": "iPhone 11 Pro Max",
            "color": "Midnight Green",
            "storage_gb": 256,
            "condition": "Used - Good",
            "price": 300.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 8,
        },
        {
            "id": 21,
            "name": "iPhone 11",
            "color": "Purple",
            "storage_gb": 128,
            "condition": "Used - Fair",
            "price": 180.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 22,
        },
        {
            "id": 22,
            "name": "iPhone XR",
            "color": "Coral",
            "storage_gb": 64,
            "condition": "Used - Good",
            "price": 150.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 17,
        },
        {
            "id": 23,
            "name": "iPhone XS Max",
            "color": "Gold",
            "storage_gb": 512,
            "condition": "Used - Excellent",
            "price": 280.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 5,
        },
        {
            "id": 24,
            "name": "iPhone X",
            "color": "Space Gray",
            "storage_gb": 64,
            "condition": "Used - Fair",
            "price": 130.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 14,
        },
        {
            "id": 25,
            "name": "iPhone 8 Plus",
            "color": "(PRODUCT)RED",
            "storage_gb": 128,
            "condition": "Used - Good",
            "price": 120.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 9,
        },
        {
            "id": 26,
            "name": "iPhone 7",
            "color": "Black",
            "storage_gb": 32,
            "condition": "Used - Fair",
            "price": 60.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 20,
        },
        {
            "id": 27,
            "name": "iPhone SE (1st Gen)",
            "color": "Rose Gold",
            "storage_gb": 32,
            "condition": "Used - Good",
            "price": 70.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 11,
        },
        {
            "id": 28,
            "name": "iPhone 6s Plus",
            "color": "Silver",
            "storage_gb": 64,
            "condition": "Used - Fair",
            "price": 50.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 28,
        },
        {
            "id": 29,
            "name": "iPhone 6",
            "color": "Space Gray",
            "storage_gb": 16,
            "condition": "Used - Acceptable",
            "price": 40.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 16,
        },
        {
            "id": 30,
            "name": "iPhone 5s",
            "color": "Gold",
            "storage_gb": 32,
            "condition": "Used - Acceptable",
            "price": 30.00,
            "is_in_stock": True,
            "is_available": True,
            "in_stock_quantity": 13,
        },
        {
            "id": 31,
            "name": "iPhone 5c",
            "color": "Blue",
            "storage_gb": 16,
            "condition": "Used - Fair",
            "price": 40.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 7,
        },
        {
            "id": 32,
            "name": "iPhone 4S",
            "color": "White",
            "storage_gb": 8,
            "condition": "Used - Acceptable",
            "price": 35.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 5,
        },
        {
            "id": 33,
            "name": "iPhone 4",
            "color": "Black",
            "storage_gb": 16,
            "condition": "Used - Acceptable",
            "price": 30.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 6,
        },
        {
            "id": 34,
            "name": "iPhone 3GS",
            "color": "White",
            "storage_gb": 8,
            "condition": "Used - Poor",
            "price": 25.00,
            "is_in_stock": False,
            "is_available": False,
            "in_stock_quantity": 0,
        },
        {
            "id": 35,
            "name": "iPhone (Original)",
            "color": "Black",
            "storage_gb": 4,
            "condition": "Collector's Item",
            "price": 15000.00,
            "is_in_stock": True,
            "is_available": False,
            "in_stock_quantity": 1,
        },
    ]
    msp = MarketplaceItems([MarketplaceItem(**item) for item in market_place])

    print(f"total distinct items in marketplace: {len(msp)}")
    print(f"total items in stock: {msp.total_in_stock_quantity()}")

    filtered = msp.filter_by("color", "Pink")
    print(f"total items in filtered marketplace: {len(filtered)}")

    found_items = filtered.fuzzy_find_by_name("iPhone 15")
    print(f"total distinct items in filtered products: {len(found_items)}")

    pprint.pprint(found_items)
