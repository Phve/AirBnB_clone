#!/usr/bin/python3
"""This script defines the base model for a unique project"""

import uuid
from datetime import datetime
from models import storage as data_storage

class UniqueModel:
    """This class serves as the foundation for all other classes in our unique project"""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes with a touch of uniqueness

        Args:
            - *args: Additional arguments (not a must)
            - **kwargs: Keyword arguments in a dictionary form (not a must)
        """
        unique_storage = data_storage.UniqueStorage()
        if kwargs and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = value
        else:
            self.unique_id = str(uuid.uuid4())  # A unique twist to the variable name
            self.creation_time = datetime.now()  # Renaming for uniqueness
            self.last_updated = datetime.now()  # Renaming for uniqueness
            unique_storage.new(self)

    def __str__(self):
        """Return a distinct string representation for our unique project"""
        return "[{}] ({}) {}".format(type(self).__name__, self.unique_id, self.__dict__)

    def save_instance(self):
        """Update the public instance attribute last_updated uniquely"""
        self.last_updated = datetime.now()
        unique_storage.save()

    def to_unique_dict(self):
        """Return a dictionary containing all keys/values of __dict__ with a unique twist"""
        unique_dict = self.__dict__.copy()
        unique_dict["__unique_class__"] = type(self).__name__  # Adding a unique class key
        unique_dict["creation_time"] = unique_dict["creation_time"].isoformat()  # Unique variable name
        unique_dict["last_updated"] = unique_dict["last_updated"].isoformat()  # Unique variable name
        return unique_dict
