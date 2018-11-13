#!/usr/bin/python3
""" Test cases for user class
"""

import unittest
import models
from models.amenity import Amenity
from models.base_model import BaseModel
import os
import json


class TestState(unittest.TestCase):
    """ Test User class
    """
    def setUp(self):
        """ Set up method """

    def tearDown(self):
        """ Tear down method """
        pass

    name = "file.json"
    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        my_amenity = Amenity()
        """
        Test keys in User dictionary
        """
        self.assertTrue(sorted(list(my_amenity.__dict__.keys())) ==
                        ['created_at', 'id', 'updated_at'], True)
        """
        Test for class attributes in User
        """
        my_amenity.name = "Pool"
        my_amenity.save()
        self.assertEqual(my_amenity.name, "Pool")
        """
        Test file.json store the object just created
        """
        if os.path.isfile(TestState.name):
            with open(TestState.name, 'r') as f:
                string = f.read()
                dic = json.loads(string)
                for key, value in dic.items():
                    if key.split('.')[1] == my_amenity.id:
                        check = 1
                        break
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
