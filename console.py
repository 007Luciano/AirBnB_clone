#!/usr/bin/python3
"""Defines the program that contains the entry point of the CLI"""

import cmd
import json
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Representation of the class Cmd from the module cmd."""
    prompt = "(hbnb) "
    __classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
    }

    def emptyline(self):
        """executes nothing upon receiving empty line"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """The end of file on input"""
        print("")
        return True

    def help_quit(self):
        """Help message for the quit command"""
        print("Quit command to exit the program")
        print()

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it
           (to the JSON file) and prints the id
        """
        if not HBNBCommand.class_provided(arg):
            return

        i_class = arg.split()[0]

        if not HBNBCommand.class_available(i_class):
            return

        obj = HBNBCommand.__classes[i_class]()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """
         Prints the string representation of an instance
         based on the class name
        """
        if not HBNBCommand.class_provided(arg):
            return

        tokens = arg.split()

        if not HBNBCommand.class_available(tokens[0]):
            return
        if len(tokens) == 2:
            i_class = tokens[0]
            i_classId = tokens[1]

        else:
            print("** instance id missing **")
            return

        if not HBNBCommand.class_available(i_class):
            return
        key = "{}.{}".format(i_class, i_classId)
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        """
        if not HBNBCommand.class_provided(arg):
            return

        tokens = arg.split()

        if not HBNBCommand.class_available(tokens[0]):
            return
        if len(tokens) == 2:
            i_class = tokens[0]
            i_classId = tokens[1]
        else:
            print("** instance id missing **")
            return
        key = "{}.{}".format(i_class, i_classId)
        if key in storage.all():
            storage.all().pop(key)
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
         Prints all string representation of all instances
         based or not on the class name
         """
        if not arg:
            obj_list = [str(obj) for obj in storage.all().values()]
            print(obj_list)
        else:
            class_name = arg.split()[0]
            if HBNBCommand.class_available(class_name):
                obj_list = [
                        str(obj) for obj in storage.all().values()
                        if type(obj).__name__ == class_name
                        ]
                print(obj_list)
        return

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute
        (save the change into the JSON file).
        """

        if not HBNBCommand.class_provided(arg):
            return

        tokens = arg.split()

        i_class = tokens[0]

        if not HBNBCommand.class_available(i_class):
            return

        if len(tokens) < 2:
            print("** instance id missing **")
            return

        i_classId = tokens[1]
        key = "{}.{}".format(i_class, i_classId)

        if key not in storage.all():
            print("** no instance found **")
            return

        if len(tokens) < 3:
            print("** attribute name missing **")
            return

        attribute_name = tokens[2]

        if len(tokens) < 4:
            print("** value missing **")
            return

        attribute_value = tokens[3]

        if hasattr(storage.all()[key], attribute_name):
            """
            Checking for attributes that can't be updated
            """
            if attribute_name == "id" or attribute_name == "created_at" or \
                    attribute_name == "updated_at":
                print("** cannot update id, created_at, or updated_at **")
                return

            """
            Casting the attribute value to the attribute type
            """
            attribute_type = type(getattr(storage.all()[key], attribute_name))
            try:
                casted_value = attribute_type(attribute_value)
            except ValueError:
                print("** invalid value type **")
                return

            setattr(storage.all()[key], attribute_name, casted_value)
            storage.all()[key].save()
        else:
            """print("** attribute doesn't exist **")"""
            setattr(storage.all()[key], attribute_name, str(attribute_value))
            storage.all()[key].save()

    def class_provided(class_name):
        """
        checks if the class name is provided
        """
        if not class_name:
            print("** class name missing **")
            return False
        return True

    def class_available(class_name):
        """
        checks if the class name is available
        """
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
