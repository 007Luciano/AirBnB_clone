#!/usr/bin/python3
"""
This module contains methods for object storage using
json object
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """abstracted storage engine
       serializes instances to a JSON file and deserializes
       JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        objectname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(objectname, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        o_dict = FileStorage.__objects
        objdict = {obj: o_dict[obj].to_dict() for obj in o_dict.keys()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(objdict, file)

    def reload(self):
        """deserializes the JSON file to __objects if it exists"""
        try:
            with open(FileStorage.__file_path) as file:
                obj_dict = json.load(file)
                for v in obj_dict.values():
                    class_name = v["__class__"]
                    del v["__class__"]
                    self.new(eval(class_name)(**v))
        except FileNotFoundError:
            return
