#!/usr/bin/python3
"""This script defines a compact City class."""

from models.base_model import BaseModel

class City(BaseModel):
    """Represent a city with state_id and name."""

    def __init__(self, *args, **kwargs):
        """Initialize a new City instance.

        Args:
            **kwargs: Keyword arguments for attributes.
        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the City instance."""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def to_dict(self):
        """Return a dictionary containing all keys/values of __dict__."""
        city_dict = super().to_dict()
        city_dict.pop('__class__', None)  # Remove __class__ for conciseness
        return city_dict

