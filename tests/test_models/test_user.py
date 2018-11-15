#!/usr/bin/python3
""" Test cases for user class
"""

import unittest
from models.user import User
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


class TestUser(unittest.TestCase):
    """ Test User class
    """
    name = "file.json"

    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        print("-- Create a new User --")
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
        print(my_user)
        self.assertEqual(my_user.first_name, "Betty")
        self.assertEqual(my_user.last_name, "Holberton")
        self.assertEqual(my_user.email, "airbnb@holbertonschool.com")
        self.assertEqual(my_user.password, "root")
        self.assertEqual(my_user.__class__.__name__, "User")
        """
        Test type of attributes
        """
        self.assertTrue(type(my_user.first_name), str)
        self.assertTrue(type(my_user.last_name), str)
        self.assertTrue(type(my_user.email), str)
        self.assertTrue(type(my_user.password), str)
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

        def test_user2(self):
            """
            Create a second user
            """
            my_user2 = User()
            my_user2.email = "user@email.com"
            my_user2.password = "user2"
            my_user2.first_name = "Hedy"
            my_user2.last_name = "Lamar"
            my_user2.save()
            print("-- Create a new User 2 --")
            self.assertEqual(my_user2.email, "user@email.com")
            self.assertEqual(my_user2.password, "user2")
            self.assertEqual(my_user2.first_name, "Hedy")
            self.assertEqual(my_user2.last_name, "Lamar")
            self.assertTrue(type(my_user2.email), str)
            self.assertEqual(type(my_user2.password), str)
            self.assertEqual(type(my_user2.first_name), str)
            self.assertEqual(type(my_user2.last_name), str)

        def test_attributes(self):
            """
            Test class for attributes
            """
            self.assertTrue(hasattr(User()), "email")
            self.assertTrue(hasattr(User()), "password")
            self.assertTrue(hasattr(User()), "first_name")
            self.assertTrue(hasattr(User()), "last_name")
            self.assertTrue(hasattr(User()), "__init__")

        def test_issubclass(self):
            """
            Test if User is a subclass of BaseModel
            """
            self.assertTrue(issubclass(User()), BaseModel)

if __name__ == '__main__':
    unittest.main()
