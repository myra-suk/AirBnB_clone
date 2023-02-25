#!/usr/bin/python3

"""Defines a class FileStorage"""
import json
from models.base_model import BaseModel
from models.review import Review
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.place import Place


class FileStorage:
    """
    Represents the class FileStorage
    Attributes:
        __file_path (str): Path to the JSON file
        __objects: Empty dictionary to store all objects
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj"""
        oname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(oname, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        odict = FileStorage.__objects
        objedict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(objedict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path) as f:
                objedict = json.load(f)
                for i in objedict.values():
                    cls_name = i["__class__"]
                    del i["__class__"]
                    self.new(eval(cls_name)(**i))
        except FileNotFoundError:
            return
