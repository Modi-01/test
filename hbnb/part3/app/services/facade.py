#!/usr/bin/python3

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # For testing we create a first admin
    def seed_admin_user(self):
        users = self.user_repo.get_all()
        if users:
            return

        admin = User(
            email="admin@test.com",
            first_name="Admin",
            last_name="User",
            password="123456",
            is_admin=True
        )
        self.user_repo.add(admin)

    # -------- User Methods --------

    def create_user(self, user_data):
        user = User(
            email = user_data['email'],
            first_name = user_data['first_name'],
            last_name = user_data['last_name'],
            password = user_data['password']        
        )
        return self.user_repo.add(user)

    def list_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("user not found")

        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

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
        
        self.amenity_repo.update(amenity_id, data)
        return self.amenity_repo.get(amenity_id)
    
    # -------- End of Amenity Methods --------

    # -------- Place Methods --------

    def create_place(self, user_id, place_data):
        user = self.user_repo.get(user_id)

        if not isinstance(user, User) or not user:
            raise ValueError("User couldn't be located.")
        
        amenities = list()

        if place_data.get('amenities') and isinstance(place_data.get('amenities'), list):
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not isinstance(amenity, Amenity) or not amenity:
                    raise ValueError("Amenity id is invalid.")
                
                amenities.append(amenity)
        
        place = Place(
            name = place_data['title'],
            owner = user,
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
        
        self.place_repo.update(place_id, data)

        return { "message": "Place updated successfully" }

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not isinstance(place, Place) or not place:
            raise ValueError("Place not found")
        
        return place.reviews


    # -------- End of Place Methods --------

    

    # -------- Review Methods --------
    def create_review(self, user_id, review_data):
        if not isinstance(review_data['text'], str) or not review_data['text'].strip():
            raise ValueError("text is required and must be a non-empty string")

        author = self.user_repo.get(user_id)
        if not isinstance(author, User) or not author:
            raise ValueError("user couldn't be found")

        place = self.place_repo.get(review_data['place_id'])
        if not isinstance(place, Place) or not place:
            raise ValueError("place must exist")

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
        
        self.review_repo.update(review_id, data)
        
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



