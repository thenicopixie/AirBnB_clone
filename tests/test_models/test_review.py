#!/usr/bin/python3
""" Test cases for user class
"""

import unittest
from models.review import Review
import os
import json


class TestReview(unittest.TestCase):
    """ Test User class
    """
    name = "file.json"

    def test_class_attributes(self):
        """ Test User class attributes """
        check = 0
        my_review = Review()
        """
        Test keys in User dictionary
        """
        self.assertTrue(sorted(list(my_review.__dict__.keys())) ==
                        ['created_at', 'id', 'updated_at'], True)
        """
        Test for class attributes in User
        """
        my_review.place_id = "123asdf678"
        my_review.user_id = "12sdfasdf"
        my_review.text = "So terrible"
        my_review.save()
        self.assertEqual(my_review.place_id, "123asdf678")
        self.assertEqual(my_review.user_id, "12sdfasdf")
        self.assertEqual(my_review.text, "So terrible")
        """
        Test file.json store the object just created
        """
        if os.path.isfile(TestReview.name):
            with open(TestReview.name, 'r') as f:
                string = f.read()
                dic = json.loads(string)
                for key, value in dic.items():
                    if key.split('.')[1] == my_review.id:
                        check = 1
                        break
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
