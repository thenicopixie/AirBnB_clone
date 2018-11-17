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
    def test_create0(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

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

    def test_show0(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_show2(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show3(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "BaseModel." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:10] + "." + string2[13:49]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy BaseModel 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Tesing `active` command"""
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy BaseModel {}".format(string[:-1]))
        all_objs = storage.all()
        key = "BaseModel." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])


if __name__ == '__main__':
    unittest.main()
