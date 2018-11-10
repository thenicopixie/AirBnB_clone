#!/usr/bin/python3
""" create a BaseModel class
"""
import uuid
from datetime import datetime
from .__init__ import storage


class BaseModel:
    """ BaseModel class
    """
    def __init__(self, *args, **kwargs):
        """ Initialize attributes
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
	#if new instantce is not in _file storage objects, make new one
        if kwargs == {}:
        #if not hasattr(storage.__object, storage):
            storage.new(self)
	#copy a new dictionary of attribute for new instance
        elif kwargs != {} and kwargs['__class__'] == self.__class__.__name__:
            for key, value in kwargs.items():
                if key == "created_at":
                    self.__dict__['created_at'] = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__['updated_at'] = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key != '__class__':
                    self.__dict__[key] = value

    def __str__(self):
        """ make string of object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """ update the with the current datetime
        """
        self.updated_at = datetime.now()
        #save new objects to File json
        storage.save()

    def to_dict(self):
        """ return a dictionary
        """
        ret_dict = {}
        for key, value in self.__dict__.items():
            ret_dict[key] = value
        ret_dict['__class__'] = self.__class__.__name__
        ret_dict['created_at'] = ret_dict['created_at'].isoformat()
        ret_dict['updated_at'] = ret_dict['updated_at'].isoformat()
        return ret_dict
