#!/usr/bin/python3
""" File Storage to serialize instances to JSON file
and deserialize JSON file to instances
"""
import json
import os.path
from datetime import datetime
from models.base_model import BaseModel

class FileStorage:
    """ FileStorage class to serializes and deserialize
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """ Sets object with key and value
        """
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[obj_key] = obj.to_dict()

    def save(self):
        """ Serializes __objects to the JSON file
        """
        #deep copy __object to new dict and convert datetime to isoformat
        dic1 = {}
        new_dic = {}
        for k, v in self.__objects.items():
            new_dic[k] = v
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as f:
                dic1 = json.loads(f.read())
                for k, v in dic1.items():
                    new_dic[k] = v
        with open(self.__file_path, 'w') as f:
            string = json.dumps(new_dic)
            f.write(string)

    def reload(self):
        """ Deserializes the JSON to __objects.
        """
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as f:
                string = f.read()
                dic = (json.loads(string))
                for key, value in dic.items():
                    self.__objects[key] = BaseModel(**value)
