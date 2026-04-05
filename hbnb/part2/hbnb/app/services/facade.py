#!/usr/bin/python3

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -------- User Methods --------

    def create_user(self, user_data):
        user = User(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        return self.user_repo.add(user)

    def list_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("user not found")

        user.update_user(data)
        return user

    # -------- End of User Methods --------

    # -------- Amenity Methods --------

    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data.get('name'))
        
        return self.amenity_repo.add(amenity)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("amenity not found")
        
        amenity.update_amenity(data)
        return amenity
    
    # -------- End of Amenity Methods --------

    # -------- Place Methods --------

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])

        if not isinstance(owner, User) or not owner:
            raise ValueError("Owner couldn't be located.")
        
        amenities = list()

        if place_data.get('amenities') and isinstance(place_data.get('amenities'), list):
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not isinstance(amenity, Amenity) or not amenity:
                    raise ValueError("Amenity id is invalid.")
                
                amenities.append(amenity)
        
        place = Place(
            name = place_data['title'],
            owner = owner,
            description = place_data['description'],
            price_per_night = place_data['price'],
            latitude = place_data['latitude'],
            longitude = place_data['longitude']
        )

        place.set_amenities(amenities)

        return self.place_repo.add(place)

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not isinstance(place, Place) or not place:
            raise ValueError("Place not found")
        
        place.update_place(data)

        return { "message": "Place updated successfully" }

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not isinstance(place, Place) or not place:
            raise ValueError("Place not found")
        
        return place.reviews


    # -------- End of Place Methods --------

    

    # -------- Review Methods --------
    def create_review(self, review_data):
        if not isinstance(review_data['text'], str) or not review_data['text'].strip():
            raise ValueError("text is required and must be a non-empty string")

        author = self.user_repo.get(review_data['user_id'])
        if not isinstance(author, User) or not author:
            raise ValueError("user couldn't be found")

        place = self.place_repo.get(review_data['place_id'])
        if not isinstance(place, Place) or not place:
            raise ValueError("place must exist")

        for review in place.reviews:
            if(review.author == author):
                raise ValueError("You already rated the place. You can edit your rating if you like. Rating id" + review.id)
        
        review = Review(text = review_data['text'], rating = review_data['rating'], author = author, place = place)
        self.review_repo.add(review)
        place.add_review(review)
        
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not isinstance(review, Review) or not review:
            raise ValueError("review not found")
        
        review.update_review(data)
        
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not isinstance(review, Review) or not review:
            raise ValueError("review not found")
        
        place = review.place
        if not isinstance(place, Place) or not place:
            raise ValueError("place must exist")
        
        review_obj = next((r for r in place.reviews if r.id == review_id), None)

        if review_obj:
            place.reviews.remove(review_obj)

        self.review_repo.delete(review_id)



