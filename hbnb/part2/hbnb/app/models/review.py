#!/usr/bin/python3
from app.models.base_model import BaseModel

class Review(BaseModel):

    def __init__(self, text, rating, author, place):
        super().__init__()
        self.text = None
        self.rating = 1
        self.author = None
        self.place = None

        self.set_text(text)
        self.set_rating(rating)
        self.set_author(author)
        self.set_place(place)

    def set_text(self, text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required and must be a non-empty string")
        
        self.text = text.strip()
        self.save()

    def set_rating(self, rating):
        if not isinstance(rating, int):
            raise ValueError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        self.rating = rating
        self.save()

    def set_author(self, author):
        self.author = author
        self.save()

    def set_place(self, place):
        self.place = place
        self.save()

    def update_review(self, data):
        self.update(data)

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.author.id,
            "place_id": self.place.id
        }
    
    def serializeList(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating
        }
