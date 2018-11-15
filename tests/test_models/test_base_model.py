#!/usr/bin/python3
"""Unittest for Base Model
"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
from models import storage
import os


def setUpModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


def tearDownModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")


class TestBase(unittest.TestCase):
    """ Test for Base Model
    """

    def test_base_00(self):
        """Test for first instance
        """
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        """
        test my_model
        """
        self.assertEqual(type(my_model.name), str)
        self.assertEqual(my_model.name, "Holberton")
        self.assertEqual(my_model.my_number, 89)
        self.assertEqual(type(my_model.id), str)
        self.assertEqual(type(my_model.created_at), datetime)
        self.assertEqual(type(my_model.updated_at), datetime)
        self.assertEqual(my_model.updated_at, my_model.created_at)
        """ Test to_dict function
        """
        my_model_json = my_model.to_dict()
        self.assertEqual(type(my_model_json), dict)
        self.assertEqual(my_model_json['created_at'],
                         my_model.created_at.isoformat())
        self.assertEqual(my_model_json['updated_at'],
                         my_model.updated_at.isoformat())
        self.assertEqual(my_model_json['__class__'],
                         my_model.__class__.__name__)
        self.assertEqual(my_model_json['my_number'], my_model.my_number)
        self.assertEqual(my_model_json['name'], my_model.name)
        """ Test create BaseModel from dictionary
        """
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_model.id, my_new_model.id)
        self.assertEqual(my_model.__dict__, my_new_model.__dict__)
        self.assertFalse(my_model is my_new_model, True)

    def test_base_01(self):
        """ Test for empty kwargs and call new function from file_storage
        """
        all_objs = storage.all()
        my_model = BaseModel()
        for key, value in all_objs.items():
            string = key.split(".")[1]
            if string == my_model.id:
                for k, v in value.__dict__.items():
                    if k != "update_at":
                        self.assertEqual(my_model.__dict__[k],
                                         all_objs[key].__dict__[k])

if __name__ == '__main__':
    unittest.main()
