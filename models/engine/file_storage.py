#!/usr/bin/python3
""" File Storage to serialize instances to JSON file
and deserialize JSON file to instances
"""
import json
import os

class FileStorage:
    """ FileStorage class to serializes and deserialize
    """
    __file_path = "models/engine/file.json"
    __objects = {}

    def all(self):
        """ Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """ Sets object with key and value
        """
        obj_key = "{}.{}".format(self.__class__.__name__, obj.id)
        self.__objects[obj_key] = obj.__dict__

    def save(self):
        """ Serializes __objects to the JSON file
        """
        #deep copy __object to new dict and convert datetime to isoformat
        ret_dict = {}
        dic1 = list(self.__objects.values())[0]
        dic2 = {}
        new_dic = {}
        key = list(self.__objects.keys())[0]
        for k, v in dic1.items():
            if k == 'created_at' or k ==  'updated_at':
                dic2[k] = v.isoformat()
            else:
                dic2[k] = v
        new_dic[key] = dic2
        string = json.dumps(new_dic)
        with open(self.__file_path, 'w') as f:
            f.write(string)

    def reload(self):
        """ Deserializes the JSON to __objects. 
        """
        try:
            with open("file.json", 'r') as f:
                for key, value in json.load(f.read).items():
                    for k, v in value:
                        if k == 'created_at' or k == 'updated_at':
                            self.__dict__[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                        else:
                            self.__dict__[k] = v
        except:
            print(self.__file_path, " not found")
            pass
