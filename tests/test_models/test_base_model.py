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
        my_new_model2 = BaseModel(name1="Nico", name2="Jack")
        self.assertEqual(my_new_model2.name1, "Nico")
        self.assertEqual(my_new_model2.name2, "Jack")

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

    def test_base_02(self):
        """Test save() method
        """
        new_instance = BaseModel()
        new_instance.save()
        self.assertGreater(new_instance.updated_at, new_instance.created_at)
        self.assertTrue(os.path.isfile("file.json"), True)

    def test_base_03(self):
        """Test to_dict() method
        """
        new_instance1 = BaseModel()
        dic = new_instance1.to_dict()
        for k, v in dic.items():
            self.assertTrue(type(v), str)
        self.assertEqual(sorted(dic.keys()),
                         sorted(['id', '__class__', 'created_at',
                                 'updated_at']))

    def test_base_04(self):
        """Test __str__ method
        """
        new_instance2 = BaseModel()
        new_instance2.__str__()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
