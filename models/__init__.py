#!/usr/bin/python3
"""
__init__ filestorage class and reloads
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()

storage.reload()
