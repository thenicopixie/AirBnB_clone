#!/usr/bin/python3
"""Unittest for Base Model"""

import unittest
from models.base_model import BaseModel
import datetime


class TestBase(unittest.TestCase):
    """ Test for Base Model
    """
    def test_base_00(self):
        """Test for first instance
        """
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        self.assertEqual(my_model.name, "Holberton")
        self.assertEqual(my_model.my_number, 89)
        self.assertEqual(type(my_model.id), str)
        self.assertEqual(type(my_model.created_at), datetime.datetime)
        self.assertEqual(type(my_model.updated_at), datetime.datetime)
        self.assertGreater(my_model.updated_at, my_model.created_at)
        """ Test to_dict function
        """
        my_model_json = my_model.to_dict()
        self.assertEqual(type(my_model_json['created_at']), str)
        self.assertEqual(type(my_model_json['updated_at']), str)
        self.assertTrue(type(my_model_json), dict)
        self.assertTrue(my_model_json.keys(), [['id'], ['created_at'],
                        ['my_number'], ['updated_at'], ['name']])
        """ Test create BaseModel from dictionary
        """
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_model.id, my_new_model.id)
        self.assertEqual(my_model.__dict__, my_new_model.__dict__)
        self.assertFalse(my_model is my_new_model, True)

if __name__ == '__main__':
    unittest.main()
