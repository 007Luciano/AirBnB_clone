#!/usr/bin/python3
"""
Defines the BaseModel class
"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the main class where others inherit from of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        for key, value in kwargs.items():
            if key != '__class__':
                if key == 'updated_at' or key == 'created_at':
                    setattr(self, key, datetime.strptime(
                        value, '%Y-%m-%dT%H:%M:%S.%f'))
                else:
                    setattr(self, key, value)

        from models import storage
        if 'id' not in kwargs:
            self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(args) == 0:
            storage.new(self)
        else:
            storage.new(self)
        # tform = "%Y-%m-%dT%H:%M:%S.%f"
        # self.id = str(uuid4())
        # self.created_at = datetime.today()
        # self.updated_at = datetime.today()
        # if len(kwargs) != 0:
        #     for k, v in kwargs.items():
        #         if k == "created_at" or k == "updated_at":
        #             self.__dict__[k] = datetime.strptime(v, tform)
        #         else:
        #             self.__dict__[k] = v
        # else:
        #     models.storage.new(self)

    def save(self):
        """
        update public instance updated_at 
        with current date
        """
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.save()
    
    def to_dict(self):
        """
        returns a dictionary of all attributes of the class instance
        include key value
        """
        instance_dict = self.__dict__.copy()
        instance_dict['__class__'] = self.__class__.__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()

        return instance_dict

    def __str__(self):
        """
        Return the str representation of object
        """
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, self.__dict__
                )
