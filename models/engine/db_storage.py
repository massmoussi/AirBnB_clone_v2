#!/usr/bin/python3

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        dbname = getenv('HBNB_MYSQL_DB')
        user = getenv('HBNB_MYSQL_USER')
        host = getenv('HBNB_MYSQL_HOST')
        passwd = getenv('HBNB_MYSQL_PWD')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine("mysql://{}:{}@{}/{}".format(user,
                                                                   passwd,
                                                                   host,
                                                                   dbname))

        if env == 'test':
            Base.metadata.drop.all()

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session = Session(bind=self.__engine, expire_on_commit=False)
        self.__session = session

    def close(self):
        """
            Close method remove the session
        """
        self.__session.close()
