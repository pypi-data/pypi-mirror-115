"""
Collection utility for Python.
"""


from typing import Any, Callable, Union
from .classes import *


class Kollektor:
    """Base class for kollektor.

    Args:
        limit (int): Collection limit.
        items (tuple): Items for collection.

    Attributes:
        limit (int): Collection limit.
        items (tuple): All of the items in the collection.
    """

    def __init__(self, limit: int = None, items: tuple = ()) -> None:
        self.limit: int = limit
        self.items: tuple = items

        if self.limit is not None:
            if len(self.items) > self.limit:
                raise LimitExceeded("Maximum limit exceeded for start items.")

    @property
    def length(self) -> int:
        """Get collection length.

        Returns:
            int: Collection length.
        """

        return len(self.items)

    def find(self, fn: Callable) -> Union[Any, Nothing]:
        """Find an object from collection.

        Args:
            fn (Callable): The function must return bool.

        Returns:
            Any: Found object.
            kollektor.Nothing
        """

        for value in self.items:
            if fn(value):
                return value

        return Nothing

    def has(self, item: Any) -> bool:
        """Check an object is in collection.

        Args:
            item (Any): The item will be checked.

        Returns:
            bool: True or False
        """

        return self.find(lambda v: v == item) != Nothing

    def append(self, *args: Any) -> tuple:
        """Append one or more object to the collection.

        Args:
            *args: The item(s) will be added.

        Returns:
            tuple: Added items.
        """

        if self.limit is not None:
            if (len(self.items) + len(args)) > self.limit:
                self.remove_index(*range(len(args)))
                self.items = (*self.items, *args, )
            else:
                self.items = (*self.items, *args, )
        else:
            self.items = (*self.items, *args, )

        return args

    def update(self, index: int, new_item: Any) -> Any:
        """Update one object from collection with index.

        Args:
            index (int): The item(s) will be replaced index.
            new_item (Any): New item.

        Returns:
            Any: New item.
        """

        self.items = tuple(v if i != index else new_item for i,
                           v in enumerate(self.items))

        return new_item

    def remove_index(self, *args: int) -> Any:
        """Remove one or more object from collection with index.

        Args:
            *args (int): List of indexs.

        Returns:
            tuple: New items.
        """

        self.items = tuple(value for index, value in enumerate(
            self.items) if index not in args)

        return self.items

    def remove(self, *args: Any) -> tuple:
        """Remove one or more object from the collection.

        Args:
            *args: The item(s) will be removed.

        Returns:
            tuple: New items.
        """

        self.items = tuple(value for value in self.items if value not in args)

        return self.items

    def first(self) -> Union[Any, Nothing]:
        """Get first element from the collection.

        Returns:
            Any: object.
            kollektor.Nothing
        """

        return self.items[0] if len(self.items) > 0 else Nothing

    def last(self) -> Union[Any, Nothing]:
        """Get last element from the collection.

        Returns:
            Any: object.
            kollektor.Nothing
        """

        return self.items[-1] if len(self.items) > 0 else Nothing

    def index(self, index: int) -> Union[Any, Nothing]:
        """Find an object from collection with index.

        Returns:
            Any: object.
            kollektor.Nothing
        """

        try:
            return self.items[index]
        except IndexError:
            return Nothing

    def filter(self, fn: Callable) -> tuple:
        """Filter objects from collection.

        Returns:
            tuple: Filtered object(s).
        """

        return tuple(value for value in self.items if fn(value))

    def each(self, fn: Callable) -> list:
        """Iterate objects from collection.

        Returns:
            list: List of returned values.
        """

        return [fn(index, value) for index, value in enumerate(self.items[:])]
