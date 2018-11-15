#!/usr/bin/python3
""" Test cases for FileStorage class
"""

import unittest
import models
from models import storage
from models.base_model import BaseModel
import os.path
from models.engine.file_storage import FileStorage
import json


def setUpModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


def tearDownModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")


class TestFileStorage(unittest.TestCase):
    """ Test case for FileStorage class
    """

    def test_all_new_save_reload(self):
        """ Test for all method
        """
        all_objs = storage.all()
        self.assertEqual(type(all_objs), dict)
        """ Test for new method
        """
        my_model = BaseModel()
        self.assertEqual(type(my_model), models.base_model.BaseModel)
        my_model.name = "Holberton"
        my_model.my_number = 89
        self.assertEqual(my_model.name, "Holberton")
        self.assertEqual(my_model.my_number, 89)
        """ Test for save method
        """
        my_model.save()
        self.assertGreater(my_model.updated_at, my_model.created_at)
        self.assertEqual(os.path.isfile('file.json'), True)
        with open('file.json', 'r') as f:
            string = f.read()
            dict1 = json.loads(string)
            for key, value in dict1.items():
                dict_id = key.split('.')[1]
                if my_model.id == dict_id:
                    for k, v in value.items():
                        if k != 'updated_at':
                            self.assertEqual(my_model.to_dict()[k],
                                             dict1[key][k])

if __name__ == '__main__':
    unittest.main()
