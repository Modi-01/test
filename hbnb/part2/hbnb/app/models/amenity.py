#!/usr/bin/python3
from app.models.base_model import BaseModel


class Amenity(BaseModel):


    def __init__(self, name):
        super().__init__()
        self.name = None
        self.set_name(name)


    def set_name(self, name):
        name = name.strip()
        print('leng')
        print(len(name))
        print(name)

        if len(name) > 50:
            return {"error": "Name must be less than 50 characters."}
        
        self.name = name
        self.save()

    def update_amenity(self, data):
        self.update(data)

    # Define return fields
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        } 
