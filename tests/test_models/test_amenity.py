#!/usr/bin/python3
""" Test cases for user class
"""
import unittest
from models.amenity import Amenity
from models import storage
import os
import json


def setUpModule():
    """ setup
    """
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


def tearDownModule():
    """ teardown
    """
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


class TestAmenity(unittest.TestCase):
    """ Test User class
    """
    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        my_amenity = Amenity()
        """
        Test keys in User dictionary
        """
        self.assertTrue(sorted(list(my_amenity.__dict__.keys())) ==
                        ['created_at', 'id', 'updated_at'], True)
        self.assertEqual(my_amenity.name, "")
        """
        Test for class attributes in User
        """
        my_amenity.name = "Pool"
        my_amenity.save()
        self.assertEqual(my_amenity.name, "Pool")
        """
        Test file.json store the object just created
        """
        if os.path.isfile("file.json"):
            with open("file.json", 'r') as f:
                string = f.read()
                dic = json.loads(string)
                for key, value in dic.items():
                    if key.split('.')[1] == my_amenity.id:
                        check = 1
                        break
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
