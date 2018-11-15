#!/usr/bin/python3
""" Test cases for user class
"""
import unittest
from models.city import City
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


class TestCity(unittest.TestCase):
    """ Test User class
    """
    name = "file.json"

    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        my_city = City()
        """
        Test keys in User dictionary
        """
        self.assertTrue(sorted(list(my_city.__dict__.keys())) ==
                        ['created_at', 'id', 'updated_at'], True)
        self.assertTrue(my_city.state_id, "")
        self.assertTrue(my_city.name, "")
        """
        Test for class attributes in User
        """
        my_city.name = "Vallejo"
        my_city.save()
        self.assertEqual(my_city.name, "Vallejo")
        """
        Test file.json store the object just created
        """
        if os.path.isfile(TestCity.name):
            with open(TestCity.name, 'r') as f:
                string = f.read()
                dic = json.loads(string)
                for key, value in dic.items():
                    if key.split('.')[1] == my_city.id:
                        check = 1
                        break
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
