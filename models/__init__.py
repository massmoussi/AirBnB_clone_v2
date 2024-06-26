#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv

t_stor = getenv("HBNB_TYPE_STORAGE")

if t_stor == "db":
    def create_storage():
        from models.engine.db_storage import DBStorage
        return DBStorage()
else:
    def create_storage():
        from models.engine.file_storage import FileStorage
        return FileStorage()

storage = create_storage()
storage.reload()
