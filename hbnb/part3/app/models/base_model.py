#!/usr/bin/python3
"""BaseModel module."""
from app.extensions import db
import uuid
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

class BaseModel(db.Model):
    """
    Base class for all entities.
    
    """
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

place_amenity = Table(
        "place_amenity",
        BaseModel.metadata,
        Column("place_id", ForeignKey("places.id"), primary_key=True),
        Column("amenity_id", ForeignKey("amenities.id"), primary_key=True),
    )
