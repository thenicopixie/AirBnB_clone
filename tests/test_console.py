#!/usr/bin/python3
""" This test for console only. It works base on properly performance of
functions and data in class BaseModel and FileStorage.
"""

import unittest
from models import storage
from models.engine.file_storage import FileStorage
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


class TestMyconsoleBaseModel(unittest.TestCase):
    """Test for console and for BaseModel and FileStorage only.
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

    def test_quit(self):
        """test quit command to quit the console by quit
        """
        cli = self.create()
        with self.assertRaises(SystemExit):
            cli.onecmd("quit")

    def test_eof(self):
        """test quit command to quit the console by EOF
        """
        cli = self.create()
        with self.assertRaises(SystemExit):
            cli.onecmd("EOF")

    def test_help(self):
        """test help function.
            Output: printing as folowwing"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("help")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string, '')
        sys.stdout.flush()

    def test_empty_string(self):
        """test help function.
            Output: printing as folowwing"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("\n")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string, '')
        sys.stdout.flush()

    def test_create0(self):
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "BaseModel." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
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
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid BaseModel and id.
        Also, create command work properly.
        Output: print object
        """
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
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
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
        """Testing destroy command with valid class name and id.
        Also, create command must work properly.
        Output: print nothing. delete object and updating in json file
        """
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
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        # sys.stdout = sys.__stdout__
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'BaseModel':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all2(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all3(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update BaseModel 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update BaseModel {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update BaseModel {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update BaseModel {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update BaseModel 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update BaseModel {} name\
                    "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a BaseModel instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all BaseModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a BaseModel instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'BaseModel' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a BaseModel instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy BaseModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("BaseModel.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "BaseModel." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('BaseModel.update("38f22813-2753-4d42",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "name",\
                    "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "phone_num",\
                    "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


class TestMyconsoleAmenity(unittest.TestCase):
    """Test for console and for Amenity and FileStorage only.
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
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "Amenity." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Amenity 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid Amenity and id.
        Also, create command work properly.
        Output: print object
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "Amenity." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Amenity {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:8] + "." + string2[11:47]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy Amenity 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Testing destroy command with valid class name and id.
        Also, create command work properly.
        Output: print nothing. delete object and updating in json file
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy Amenity {}".format(string[:-1]))
        all_objs = storage.all()
        key = "Amenity." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'Amenity':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all3(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all5(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Amenity 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Amenity {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Amenity {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update Amenity {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Amenity 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Attribute value is not single world and in side double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update Amenity {} name\
                    "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a Amenity instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Amenity.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Amenity")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a Amenity instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Amenity.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'Amenity' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a Amenity instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Amenity.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Amenity {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Amenity.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Amenity Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Amenity.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy Amenity Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("Amenity.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "Amenity." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                   "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('Amenity.update("38f22813-2753-4d42",\
                                   "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Amenity.update({}, "name",\
                   "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Amenity.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Amenity.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Amenity.update({}, "phone_num",\
                   "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Amenity")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Amenity.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "Amenity.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


class TestMyconsoleCity(unittest.TestCase):
    """Test for console and for City and FileStorage only.
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
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "City." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show City 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid City and id.
        Also, create command work properly.
        Output: print object
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "City." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show City {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:5] + "." + string2[8:44]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy City 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Testing destroy command with valid class name and id.
        Also, create command work properly.
        Output: print nothing. delete object and updating in json file
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy City {}".format(string[:-1]))
        all_objs = storage.all()
        key = "City." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'City':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all2(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all3(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update City 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update City {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update City {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update City {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update City 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update City {} name\
                   "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a City instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("City.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all City")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a City instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("City.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'City' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a City instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("City.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show City {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("City.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show City Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("City.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy City Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("City.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "City." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('City.update("38f22813-2753-4d42",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('City.update({}, "name",\
                    "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('City.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('City.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('City.update({}, "phone_num",\
                    "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create City")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('City.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "City.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


class TestMyconsolePlace(unittest.TestCase):
    """Test for console and for Place and FileStorage only.
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
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "Place." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Place 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid Place and id.
        Also, create command work properly.
        Output: print object
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "Place." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Place {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:6] + "." + string2[9:45]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy Place 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Testing destroy command with valid class name and id.
        Also, create command work properly.
        Output: print nothing. delete object and updating in json file
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy Place {}".format(string[:-1]))
        all_objs = storage.all()
        key = "Place." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'Place':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all3(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all5(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Place 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Place {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Place {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update Place {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Place 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update Place {} name\
                   "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_update9(self):
        """ Testing update command with all valid data.
        Attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update Place {} max_guest 5".format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'max_guest'):
            attr_val = all_objs[key].__dict__['max_guest']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 5)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'max_guest' in dic[key].keys():
                        j_attr_val = dic[key]['max_guest']
                        break
        self.assertEqual(j_attr_val, 5)

    def test_update10(self):
        """ Testing update command with all valid data.
        Attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update Place {} latitude 1.1".format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'latitude'):
            attr_val = all_objs[key].__dict__['latitude']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 1.1)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'latitude' in dic[key].keys():
                        j_attr_val = dic[key]['latitude']
                        break
        self.assertEqual(j_attr_val, 1.1)

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a Place instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Place.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Place")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a Place instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Place.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'Place' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a Place instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Place.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Place {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Place.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Place Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Place.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy Place Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("Place.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "Place." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('Place.update("38f22813-2753-4d42",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Place.update({}, "name",\
                    "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Place.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Place.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Place.update({}, "phone_num",\
                    "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Place")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Place.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "Place.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


class TestMyconsoleReview(unittest.TestCase):
    """Test for console and for Review and FileStorage only.
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
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "Review." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Review 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid Review and id.
        Also, create command work properly.
        Output: print object
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "Review." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Review {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:7] + "." + string2[10:46]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy Review 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Testing destroy command with valid class name and id.
        Also, create command work properly.
        Output: print nothing. delete object and updating in json file
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy Review {}".format(string[:-1]))
        all_objs = storage.all()
        key = "Review." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'Review':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all2(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all3(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Review 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Review {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Review {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update Review {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update Review 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update Review {} name\
                   "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a Review instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Review.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all Review")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a Review instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Review.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'Review' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a Review instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Review.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Review {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Review.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show Review Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("Review.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy Review Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("Review.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "Review." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('Review.update("38f22813-2753-4d42",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Review.update({}, "name",\
                    "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Review.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Review.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Review.update({}, "phone_num",\
                    "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create Review")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('Review.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "Review.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


class TestMyconsoleState(unittest.TestCase):
    """Test for console and for State and FileStorage only.
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
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "State." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show State 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid State and id.
        Also, create command work properly.
        Output: print object
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "State." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show State {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:6] + "." + string2[9:45]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy State 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Testing destroy command with valid class name and id.
        Also, create command work properly.
        Output: print nothing. delete object and updating in json file
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy State {}".format(string[:-1]))
        all_objs = storage.all()
        key = "State." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'State':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all2(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all3(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update State 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update State {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update State {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update State {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update State 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update State {} name\
                   "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a State instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("State.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all State")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a State instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("State.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'State' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a State instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("State.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show State {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("State.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show State Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("State.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy State Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("State.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "State." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('State.update("38f22813-2753-4d42",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('State.update({}, "name",\
                    "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('State.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('State.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('State.update({}, "phone_num",\
                    "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create State")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('State.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "State.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


class TestMyconsoleUser(unittest.TestCase):
    """Test for console and for User and FileStorage only.
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
        """test create command without class nameself.
            Output: printing "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_create1(self):
        """test create command with valid class name.
        Output: id number of instance
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        key = "User." + string[:-1]
        all_objs = storage.all()
        self.assertTrue(key in list(all_objs.keys()))
        filename = FileStorage._FileStorage__file_path
        lis = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] in lis)
        sys.stdout.flush()

    def test_create2(self):
        """Tesing create command with non-existing class.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_show1(self):
        """Testing show command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
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
        """Testing show command without id.
        Output: print "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show User")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** instance id missing **")
        sys.stdout.flush()

    def test_show3(self):
        """Testing show command without id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show User 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_show4(self):
        """Testing show command with valid User and id.
        Also, create command work properly.
        Output: print object
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = "User." + string[:-1]
        self.mock_stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show User {}".format(string))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        string3 = string2[1:5] + "." + string2[8:44]
        self.assertEqual(string1, string3)
        self.mock_stdout.flush()

    def test_destroy0(self):
        """Testing destroy command without class name.
        Output: print "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_destroy1(self):
        """Testing destroy command with non-existing class name.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_destroy2(self):
        """Testing destroy command with non-existing id.
        Output: print "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy User 1234567")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** no instance found **")
        sys.stdout.flush()

    def test_destroy3(self):
        """Testing destroy command with valid class name and id.
        Also, create command work properly.
        Output: print nothing. delete object and updating in json file
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("destroy User {}".format(string[:-1]))
        all_objs = storage.all()
        key = "User." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_all0(self):
        """Testing all command with valid class name.
        Also, create command work properly.
        Output: print all object that have same the class name
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        all_objs = storage.all()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        for key in all_objs.keys():
            lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all1(self):
        """Testing all command with out class name.
        Also, create command work properly.
        Output: print all object
        """
        filename = FileStorage._FileStorage__file_path
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        self.mock_stdout.flush()
        """ capture output after all command """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all User")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.mock_stdout.flush()
        """capture output after print all objects """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        lis = []
        all_objs = storage.all()
        for key in all_objs.keys():
            if key.split('.')[0] == 'User':
                lis += [all_objs[key].__str__()]
        print(lis)
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(len(string1), len(string2))
        self.assertEqual(string1, string2)
        self.mock_stdout.flush()

    def test_all2(self):
        """Tesing all command with non-existing class.
        Output: print "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "** class doesn't exist **")
        sys.stdout.flush()

    def test_all3(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_all4(self):
        """Tesing all command when there is not object existing.
        Also, destroy command work properly.
        This test works only the objests are stored in dictionary
        with key is "<class name>.<id number>" and value is object itself
        Output: print []
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all User")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        string1 = string[:-1]
        self.assertEqual(string1, "[]")
        sys.stdout.flush()

    def test_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class name missing **")
        sys.stdout.flush()

    def test_update1(self):
        """ Testing update command with non-existing class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update MyModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_update2(self):
        """ Testing update command without id number
        Ouput: print error message "** instance id missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update User")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** instance id missing **")
        sys.stdout.flush()

    def test_update3(self):
        """ Testing update command with non-existing id number
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update User 1234")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_update4(self):
        """ Testing update command without attribute name
        Also, create command work properly.
        Ouput: print error message "** attribute name missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update User {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** attribute name missing **")
        sys.stdout.flush()

    def test_update5(self):
        """ Testing update command without attribute value
        Also, create command work properly.
        Ouput: print error message "** value missing **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update User {} name".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        self.assertEqual(string2[:-1], "** value missing **")
        sys.stdout.flush()

    def test_update6(self):
        """ Testing update command with all valid data.
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd("update User {} name Betty".format(string1[:-1]))
        all_objs = storage.all()
        key = "User.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty")

    def test_update7(self):
        """ Testing update command with no object existing
        Also, destroy command works properly
        Ouput: print "** no instance found **"
        """
        cli = self.create()
        all_objs = storage.all()
        destroy_info = []
        temp = []
        for k in all_objs.keys():
            temp = k.split('.')
            destroy_info += [temp[0] + " " + temp[1]]
        for item in destroy_info:
            cli.onecmd("destroy {}".format(item))
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("update User 1234")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        self.assertEqual(string1[:-1], "** no instance found **")

    def test_update8(self):
        """ Testing update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create User")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('update User {} name\
                   "Betty Holberton"'.format(string1[:-1]))
        all_objs = storage.all()
        key = "User.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_all0(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ create a BaseModel instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all BaseModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_all1(self):
        """ Testing all functions by advance"
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.all()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("all MyModel")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string1, string2)

    def test_advance_count(self):
        """ Testing count function"
        """
        count = 0
        cli = self.create()
        """ create a BaseModel instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.count()")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ count number of objects """
        for k in storage.all().keys():
            if 'BaseModel' == k.split(".")[0]:
                count += 1
        self.assertEqual(string1[:-1], str(count))

    def test_advance_show0(self):
        """ Testing show function by advance"
        """
        cli = self.create()
        """ create a BaseModel instance """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.show({})".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel {}".format(string1[:-1]))
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show1(self):
        """ Testing show function by advance"
        No id existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show BaseModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_show2(self):
        """ Testing show function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.show('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("show MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy0(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("MyModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy MyModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy1(self):
        """ Testing destroy function by advance"
        No class name existing
        """
        cli = self.create()
        """ print it in advance function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("BaseModel.destroy('Holberton')")
        sys.stdout = sys.__stdout__
        string2 = captureOutput.getvalue()
        sys.stdout.flush()
        """ print it in regular function """
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("destroy BaseModel Holberton")
        sys.stdout = sys.__stdout__
        string3 = captureOutput.getvalue()
        sys.stdout.flush()
        self.assertEqual(string2, string3)

    def test_advance_destroy2(self):
        """ Testing destroy function by advance"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.mock_stdout.flush()
        cli.onecmd("BaseModel.destroy({})".format(string[:-1]))
        all_objs = storage.all()
        key = "BaseModel." + string[:-1]
        self.assertFalse(key in list(all_objs.keys())[0])
        filename = FileStorage._FileStorage__file_path
        lis = []
        """ check in json file """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
            for v in dic.values():
                lis += [v['id']]
        self.assertTrue(string[:-1] not in lis)

    def test_advance_update0(self):
        """ Testing update command without class name
        Ouput: print error message "** class doesn't exist **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('MyModel.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** class doesn't exist **")
        sys.stdout.flush()

    def test_advance_update1(self):
        """ Testing update command without class name
        Ouput: print error message "** no instance found **"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd('BaseModel.update("38f22813-2753-4d42",\
                                    "first_name", "John")')
        sys.stdout = sys.__stdout__
        string = captureOutput.getvalue()
        self.assertEqual(string[:-1], "** no instance found **")
        sys.stdout.flush()

    def test_advance_update2(self):
        """ Testing advance update command with all valid data.
        Test attribute value is not a single world and in double quote
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "name",\
                    "Betty Holberton")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'name'):
            attr_val = all_objs[key].__dict__['name']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "Betty Holberton")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'name' in dic[key].keys():
                        j_attr_val = dic[key]['name']
                        break
        self.assertEqual(j_attr_val, "Betty Holberton")

    def test_advance_update3(self):
        """ Testing advance update command with all valid data.
        Test attribute value is float type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "age", 8.9)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 8.9)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 8.9)

    def test_advance_update4(self):
        """ Testing advance update command with all valid data.
        Test attribute value is integer type
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "age", 89)'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], 'age'):
            attr_val = all_objs[key].__dict__['age']
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, 89)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and 'age' in dic[key].keys():
                        j_attr_val = dic[key]['age']
                        break
        self.assertEqual(j_attr_val, 89)

    def test_advance_update5(self):
        """ Testing advance update command with all valid data.
        Test attribute value is string type with number
        Also, create command work properly.
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, "phone_num",\
                    "123-456-789")'.format(string1[:-1]))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        if hasattr(all_objs[key], "phone_num"):
            attr_val = all_objs[key].__dict__["phone_num"]
        else:
            attr_val = 'fake'
        self.assertEqual(attr_val, "123-456-789")
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic = json.loads(f.read())
                for k in dic.keys():
                    if k == key and "phone_num" in dic[key].keys():
                        j_attr_val = dic[key]["phone_num"]
                        break
        self.assertEqual(j_attr_val, "123-456-789")

    def test_advance_update6(self):
        """ Testing advance update command with all valid data.
        Also, create command work properly.
        update by dictionary
        Ouput: save the updated attribute to object and json file"
        """
        cli = self.create()
        dic = {"first_name": "John", "age": 89,
               "phone_num": "123-456-789", "promotion": 1.2}
        captureOutput = io.StringIO()
        sys.stdout = captureOutput
        cli.onecmd("create BaseModel")
        sys.stdout = sys.__stdout__
        string1 = captureOutput.getvalue()
        sys.stdout.flush()
        cli.onecmd('BaseModel.update({}, {})'.format(string1[:-1], dic))
        all_objs = storage.all()
        key = "BaseModel.{}".format(string1[:-1])
        for k, v in dic.items():
            if hasattr(all_objs[key], k):
                attr_val = all_objs[key].__dict__[k]
            else:
                attr_val = 'fake'
            self.assertEqual(attr_val, v)
        """ check in json file """
        filename = FileStorage._FileStorage__file_path
        j_attr_val = 'fake'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                dic1 = json.loads(f.read())
                for k1 in dic1.keys():
                    for k2, v2 in dic.items():
                        if k1 == key and k2 in dic1[key].keys():
                            j_attr_val = dic1[key][k2]
                            break
                            self.assertEqual(j_attr_val, v2)
        self.assertNotEqual(j_attr_val, 'fake')


if __name__ == '__main__':
    unittest.main()
