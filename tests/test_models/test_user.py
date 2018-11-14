#!/usr/bin/python3
""" Test cases for user class
"""

import unittest
from models.city import City
import os
import json


class TestUser(unittest.TestCase):
    """ Test User class
    """
    name = "file.json"

    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        my_user = User()
        """
        Test keys in User dictionary
        """
        self.assertTrue(sorted(list(my_user.__dict__.keys())) ==
                        ['created_at', 'id', 'updated_at'], True)
        """
        Test for class attributes in User
        """
        my_user.first_name = "Betty"
        my_user.last_name = "Holberton"
        my_user.email = "airbnb@holbertonschool.com"
        my_user.password = "root"
        my_user.save()
        self.assertEqual(my_user.first_name, "Betty")
        self.assertEqual(my_user.last_name, "Holberton")
        self.assertEqual(my_user.email, "airbnb@holbertonschool.com")
        self.assertEqual(my_user.password, "root")
        self.assertEqual(my_user.__class__.__name__, "User")
        """
        Test file.json store the object just created
        """
        if os.path.isfile(TestUser.name):
            with open(TestUser.name, 'r') as f:
                string = f.read()
                dic = json.loads(string)
                for key, value in dic.items():
                    if key.split('.')[1] == my_user.id:
                        check = 1
                        break
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
