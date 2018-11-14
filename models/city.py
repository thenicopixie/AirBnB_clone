#!/usr/bin/python3
""" Create City class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """ City class that inherits from BaseModel class
    """
    state_id = ""
    name = ""
