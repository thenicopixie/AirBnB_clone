#!/usr/bin/python3
"""Unittest for Init file
"""
import unittest
from datetime import datetime
import models
from models import storage
from models.base_model import BaseModel
import os


def setUpModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


def tearDownModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")


class TestInit(unittest.TestCase):
    """ Test for Init file
    """

    def test_init00(self):
        """ Test import module
        """
        new_instance = BaseModel()
        all_objs = models.storage.all()
        self.assertTrue(type(all_objs), dict)


if __name__ == '__main__':
    unittest.main()
