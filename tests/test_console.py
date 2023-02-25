#!/usr/bin/python3

""" Defines unittests for our AirBnB console
Unitest classes:
    TestConsole_prompt
    TestConsole_help
    TestConsole_exit
    TestConsole_create
    TestConsole_show
    TestConsole_all
    TestConsole_destroy
    TestConsole_update
"""
import sys
import unittest
from models import storage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models.engine.file_storage import FileStorage
import os


class TestConsole_prompt(unittest.TestCase):
    """ Unittests for testing the prompt of our command interpreter"""

    def test_prompt_string(self):
        self.assertEqual("(hbnb)", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", f.getvalue().strip())


class TestConsole_help(unittest.TestCase):
    """Unittests for testing the help function of the command interpreter
    """

    def test_help_quit(self):
        prints = "Quit command to exit the interpreter"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(prints, f.getvalue().strip())

    def test_help_create(self):
        prints = ("Usage: create <class>\n        "
                  "Creates a new instance and prints it's id")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(prints, f.getvalue().strip())

    def test_help_EOF(self):
        prints = "EOF signal to quit the program"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(prints, f.getvalue().strip())

    def test_help_show(self):
        prints = ("Usage: show <class> <id>\n        "
                  "Prints the string representation of an instance")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(prints, f.getvalue().strip())


class TestConsole_exit(unittest.TestCase):
    """Unittests for the Exit command"""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


if __name__ == '__main__':
    unittest.main()
