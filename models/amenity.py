#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey


class Amenity(BaseModel, Base):
    if models.t_stor == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes reviews"""
        super().__init__(*args, **kwargs)
