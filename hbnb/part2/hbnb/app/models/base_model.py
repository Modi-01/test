#!/usr/bin/python3
"""BaseModel module."""

import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all entities.
    
    """

    def __init__(self):
        
        self.id = str(uuid.uuid4())
        now = datetime.utcnow()
        self.created_at = now
        self.updated_at = now

    def save(self):
        
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

