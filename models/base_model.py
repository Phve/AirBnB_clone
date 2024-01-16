#!/usr/bin/python3
"""This script defines the base model for a unique project"""

import uuid
from datetime import datetime
import models

class BaseModel:
    """This class serves as the foundation for all other classes in our unique project"""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes with a touch of uniqueness

        Args:
            - *args: Additional arguments (not a must)
            - **kwargs: Keyword arguments in a dictionary form (not a must)
        """
        if kwargs and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4()) 
            self.created_at = datetime.now() 
            self.updated_at = datetime.now()  
            models.storage.new(self)

    def __str__(self):
        """Return a distinct string representation for our unique project"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update the public instance attribute last_updated uniquely"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = type(self).__name__
        obj_dict["created_at"] = obj_dict["created_at"].isoformat()
        obj_dict["updated_at"] = obj_dict["updated_at"].isoformat()
        return obj_dict
