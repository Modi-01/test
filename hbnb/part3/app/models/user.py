#!/usr/bin/python3

from app.models.base_model import BaseModel
from app import bcrypt
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship("Place", backref="owner", lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __init__(self, email, first_name, last_name, password, is_admin=False):
        super().__init__()
        self.set_email(email, autosave=False)
        self.set_first_name(first_name, autosave=False)
        self.set_last_name(last_name, autosave=False)
        self.set_password(password)
        self.is_admin = is_admin
        
        self.save()

    def set_email(self, email, autosave=True):

        email = email.strip().lower()
        self.email = email

    def set_password(self, password, autosave=True):
        if not isinstance(password, str) or not password:
            raise ValueError("password is required and must be a non-empty string")
        
        if len(password) < 6:
            raise ValueError("password must be at least 6 characters")

        self.hash_password(password)

    def set_first_name(self, first_name, autosave=True):
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name is required and must be a non-empty string")

        first_name = first_name.strip()

        if len(first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")

        self.first_name = first_name

    def set_last_name(self, last_name, autosave=True):
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name is required and must be a non-empty string")
        
        last_name = last_name.strip()
        
        if len(last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        
        self.last_name = last_name


    def set_is_admin(self, is_admin, autosave=True):
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")
        
        self.is_admin = is_admin
        

    def update_user(self, data):
        self.update(data)


    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    # Define return fields
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        } 
