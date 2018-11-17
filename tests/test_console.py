#!/usr/bin/python3
""" Test cases for console
"""

import unittest
from models import storage
import os
import io
import json
import sys
from console import HBNBCommand
from unittest.mock import create_autospec


def setUpModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")
    storage._FileStorage__objects.clear()


def tearDownModule():
    if os.path.isfile("file.json"):
        os.remove("file.json")


class TestMyconsole(unittest.TestCase):
    """Test the console
    """

    def setUp(self):
        """ SetUp
        """
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self, server=None):
        """ create function
        """
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def test_create1(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        all_objs = storage.all()
        key = "BaseModel." + string[:-1]
        self.assertEqual(key, list(all_objs.keys())[0])
        sys.stdout.flush()

    def test_create2(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

if __name__ == '__main__':
    unittest.main()
