#!/usr/bin/python3
""" Test cases for user class
"""

import unittest
import models
from models.user import User
from models.base_model import BaseModel
import os

class TestUser(unittest.TestCase):
    """ Test User class
    """
    def setUp(self):
        """ Set up method """
        name = "file.json"
        #if os.path.isfile(name):
        #    os.remove(name)

    def tearDown(self):
        """ Tear down method """
        pass

    name = "file.json"
    def test_class_attributes(self):
        """ Test User class attributes """
        my_user = User()
        """
        Test keys in User dictionary
        """
        print(sorted(list(my_user.__dict__.keys())), type(list(my_user.__dict__.keys())))
        self.assertTrue(sorted(list(my_user.__dict__.keys())) == ['created_at', 'id', 'updated_at'], True)
        """
        Test for class attributes in User
        """
        my_user.first_name = "Betty"
        my_user.last_name = "Holberton"
        my_user.email = "airbnb@holbertonschool.com"
        my_user.password = "root"
        with open(TestUser.name, "r") as f:
            wordcount = len(f.read())
            print("BEFORE remove", wordcount)
        if os.path.isfile(TestUser.name):
            print("check")
            os.remove(TestUser.name)
        my_user.save()
        """
        Count words in file and compare
        """
        with open(TestUser.name, "r") as f:
            wordcount = len(f.read())
        self.assertEqual(wordcount, 43)
        self.assertEqual(my_user.first_name, "Betty")
        self.assertEqual(my_user.last_name, "Holberton")
        self.assertEqual(my_user.email, "airbnb@holbertonschool.com")
        self.assertEqual(my_user.password, "root")
        self.assertEqual(my_user.__class__.__name__, "User")
