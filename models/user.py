#!/usr/bin/python3
""" User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """ Class User that inherits from BaseModel class.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """ Initialize arguments for user class. """
        super().__init__(*args, **kwargs)
