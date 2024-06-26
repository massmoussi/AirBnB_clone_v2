#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
import models
from sqlalchemy import Column, DateTime, String

if models.t_stor == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if models.t_stor == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = kwargs.get('id', str(uuid.uuid4()))

        self.created_at = kwargs.get('created_at', None)
        if self.created_at:
            self.created_at = datetime.strptime(self.created_at,
                                                '%Y-%m-%dT%H:%M:%S.%f')
        else:
            self.created_at = datetime.now()

        self.updated_at = kwargs.get('updated_at', None)
        if self.updated_at:
            self.updated_at = datetime.strptime(self.updated_at,
                                                '%Y-%m-%dT%H:%M:%S.%f')
        else:
            self.updated_at = datetime.now()

        if '__class__' in kwargs:
            del kwargs['__class__']
        self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()

        dictionary.pop('_sa_instance_state', None)

        dictionary['__class__'] = type(self).__name__
        time = ''

        if isinstance(dictionary['created_at'], str):
            dictionary['created_at'] = datetime.strptime(
                dictionary['created_at'], '%Y-%m-%dT%H:%M:%S.%f')

        if isinstance(dictionary['updated_at'], str):
            dictionary['updated_at'] = datetime.strptime(
                dictionary['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()

        return dictionary

    def delete(self):
        """
            delete the current instance
        """
        from models import storage
        storage.delete(self)
