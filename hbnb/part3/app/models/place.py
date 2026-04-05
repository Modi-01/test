#!/usr/bin/python3
from app.models.base_model import BaseModel
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    # id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        backref='places',
        lazy=True
    )

    def __init__(self, name, owner, description="", price_per_night=0.0,
                 latitude=0.0, longitude=0.0):
        super().__init__()
        self.title = None
        self.description = None
        self.price = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.owner = None

        self.reviews = []
        self.amenities = []

        self.set_name(name)
        self.set_owner(owner)
        self.set_description(description)
        self.set_price_per_night(price_per_night)
        self.set_latitude(latitude)
        self.set_longitude(longitude)


    def set_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name is required and must be a non-empty string")
        name = name.strip()
        if len(name) < 5 or len(name) > 100:
            raise ValueError("name must be greater than 5 characters and not exceed 100 characters")
        self.title = name
        self.save()

    def set_description(self, description):
        if description is None:
            description = ""
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        self.description = description
        self.save()

    def set_price_per_night(self, price_per_night):
        if not isinstance(price_per_night, float):
            raise ValueError("Price must be a decimal")
        if price_per_night <= 0:
            raise ValueError("Price must be > 0")
        self.price = price_per_night
        self.save()

    def set_latitude(self, latitude):
        if not isinstance(latitude, (int, float)):
            raise ValueError("latitude must be a number")
        latitude = float(latitude)
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be within -90.0 to 90.0")
        self.latitude = latitude
        self.save()

    def set_longitude(self, longitude):
        if not isinstance(longitude, (int, float)):
            raise ValueError("longitude must be a number")
        longitude = float(longitude)
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be within -180.0 to 180.0")
        self.longitude = longitude
        self.save()

    def set_owner(self, owner):
        self.owner = owner
        self.save()

    def set_amenities(self, amenities):
        self.amenities = amenities
        self.save()

    def add_review(self, review_obj):
        if review_obj.place is not self:
            raise ValueError("review.place must reference this Place instance")

        self.reviews.append(review_obj)
        self.save()

    def update_place(self, data):
        self.update(data)

    def serializeList(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price
        }

    def serializeNew(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id
        }
    
    def serializeById(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "price": self.price,
            # "owner": self.owner.serialize(),
            # "amenities": [amenity.serialize() for amenity in self.amenities],
            # "reviews": [review.serializeList() for review in self.reviews]
        }
