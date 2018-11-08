#!/usr/bin/python3
"""Unittest for Base Model"""

import unittest
from models.base_model import BaseModel


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
        my_model_json = my_model.to_dict()
        self.assertEqual(type(my_model_json['created_at']), str)
        self.assertEqual(type(my_model_json['updated_at']), str)
        self.assertTrue(type(my_model_json), dict)
        self.assertTrue(my_model_json.keys(), [['id'], ['created_at'],
                                                    ['my_number'], ['updated_at'],
                                                    ['name']])

if __name__ == '__main__':
    unittest.main()
