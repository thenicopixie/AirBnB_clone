#!/usr/bin/python3
""" Test cases for console
"""

import unittest
from models import storage
import os
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
        """ setUp function
        """
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self, server=None):
        """ Test create
        """
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def _last_write(self, nr=None):
        """:return: last `n` output lines"""
        if nr is None:
            return self.mock_stdout.write.call_args[0][0]
        return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[-nr:]))

    def test_active(self):
        """Tesing `active` command"""
        cli = self.create()
        self.assertFalse(cli.onecmd("BaseModel"))
        self.assertFalse(self.mock_stdout.flush.called)
        string = self._last_write()
        self.assertTrue(string, self._last_write())


if __name__ == '__main__':
    unittest.main()