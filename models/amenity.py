#!/usr/bin/python3

""" Defines the Amenity class """

import uuid
from datetime import datetime
from models import storage
from models.base_model import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity
    
    Attributes:
        name (str): The name of the amenity.
    """

    name = ""
