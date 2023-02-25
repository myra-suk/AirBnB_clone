#!/usr/bin/python3

"""Defines the AirBnB command line interpreter"""
import cmd
import sys
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User
from models.state import State


def parse_line(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """ Represents our AirBnB interpreter
    Attributes:
        prompt (str): Command line prompt
    """

    prompt = "(hbnb)"
    __classes = {
            "User",
            "State",
            "Amenity",
            "Place",
            "Review",
            "City",
            "BaseModel"
    }

    def emptyline(self):
        """Does nothing when it receives an empty line"""
        self.non_interactive_check()
        pass

    def do_quit(self, arg):
        """Quit command to exit the interpreter"""
        return True

    def do_EOF(self, arg):
        """EOF signal to quit the program"""
        print("")
        return True

    @staticmethod
    def non_interactive_check():
        if sys.stdin.isatty() is False:
            print("")

    def do_create(self, arg):
        """
        Usage: create <class>
        Creates a new instance and prints it's id
        """
        self.non_interactive_check()
        argl = parse_line(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Usage: show <class> <id>
        Prints the string representation of an instance
        """
        self.non_interactive_check()
        argl = parse_line(arg)
        objedict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objedict:
            print("** no instance found **")
        else:
            print(objedict["{}.{}".format(argl[0], argl[1])])

    def do_count(self, arg):
        """Usage: count <class>
        Retrieve the number of instances of a given class
        """
        argl = parse_line(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_destroy(self, arg):
        """
        Usage: destroy <class> <id>
        Deletes an instance based on class name and id
        Saves the change into the JSON file
        """
        self.non_interactive_check()
        argl = parse_line(arg)
        objedict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objedict.keys():
            print("** no instance found **")
        else:
            del objedict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Usage: all or all <class>
        Prints all string representation of all instances
        """
        self.non_interactive_check()
        argl = parse_line(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objectl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objectl.append(obj.__str__())
                elif len(argl) == 0:
                    objectl.append(obj.__str__())
            print(objectl)

    def do_update(self, arg):
        """
        Usage: update <class name> <id> <attribute name> "<attribute value>
        Updates an instance based on the class name and id
        Saves the change in the JSON file
        """
        self.non_interactive_check()
        argl = parse_line(arg)
        objedict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objedict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objedict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objedict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
