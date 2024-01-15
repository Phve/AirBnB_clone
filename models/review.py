#!/usr/bin/python3
"""This module creates a Review class"""

from .base_model import BaseModel


class Review(BaseModel):
    """Class for managing review objects
    Attributes:
        place_id (str): The Place id.
        reviewer_id (str): The Reviewer id.
        content (str): The content of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
