#!/usr/bin/python3
""" create a BaseModel class
"""
import uuid
import datetime

class BaseModel:
    """ BaseModel class
    """

    id = str(uuid.uuid4())
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()

    def __str__(self):
        """ make string of object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """ update the with the current datetime
        """
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """ return a dictionary 
        """
        ret_dict = {}
        for key, value in self.__dict__.items():
            ret_dict[key] = value
        ret_dict['created_at'].isoformat()
        ret_dict['updated_at'].isoformat()
        ret_dict['__class__'] = self.__class__.__name__
        return ret_dict
