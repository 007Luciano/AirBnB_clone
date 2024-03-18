#!/usr/bin/python3
"""Defines the user class that inherits from BaseModel"""

from models.base_model import BaseModel


class User(BaseModel):
    """Represents User"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
