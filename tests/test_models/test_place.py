#!/usr/bin/python3
""" Test cases for user class
"""

import unittest
from models.place import Place
from models import storage
import os
import json


def setUpModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


def tearDownModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")


class TestPlace(unittest.TestCase):
    """ Test User class
    """
    name = "file.json"

    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        my_place = Place()
        """
        Test keys in User dictionary
        """
        self.assertTrue(sorted(list(my_place.__dict__.keys())) ==
                        ['created_at', 'id', 'updated_at'], True)
        """
        Test for class attributes in User
        """
        my_place.name = "Hotel"
        my_place.city_id = "12345678"
        my_place.user_id = "12345678"
        my_place.description = "12345678"
        my_place.number_rooms = 3
        my_place.number_bathrooms = 2
        my_place.max_guest = 4
        my_place.price_by_night = 100
        my_place.latitude = 123456.789
        my_place.longitude = 123456.789
        my_place.amenity_ids = ["Pool", "Gym"]
        my_place.save()
        self.assertEqual(my_place.name, "Hotel")
        self.assertEqual(my_place.city_id, "12345678")
        self.assertEqual(my_place.user_id, "12345678")
        self.assertEqual(my_place.description, "12345678")
        self.assertEqual(my_place.number_rooms, 3)
        self.assertEqual(my_place.number_bathrooms, 2)
        self.assertEqual(my_place.max_guest, 4)
        self.assertEqual(my_place.price_by_night, 100)
        self.assertEqual(my_place.latitude, 123456.789)
        self.assertEqual(my_place.longitude, 123456.789)
        self.assertEqual(my_place.amenity_ids, ["Pool", "Gym"])
        """
        Test file.json store the object just created
        """
        if os.path.isfile(TestPlace.name):
            with open(TestPlace.name, 'r') as f:
                string = f.read()
                dic = json.loads(string)
                for key, value in dic.items():
                    if key.split('.')[1] == my_place.id:
                        check = 1
                        break
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
