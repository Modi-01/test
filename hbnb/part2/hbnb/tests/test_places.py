#!/usr/bin/python3
import unittest
import uuid
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def _seed_valid_place_dependencies(self):
        """Create a valid user and place only to obtain IDs for review tests."""
        unique = uuid.uuid4().hex[:8]

        # create user (setup dependency only)
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": f"jane.{unique}@example.com"
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.get_json()['id']        

        return user_id
        

    def test_create_place(self):
        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)

    def test_create_place_invalid_user_id(self):

        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id + "-2"
        })
        self.assertEqual(place_response.status_code, 400)

    #Testing price must be decimal value
    def test_create_place_invalid_price(self):

        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 20,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 400)

    #Testing title
    def test_create_place_invalid_title(self):

        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 400)

    #Testing title emtpy
    def test_create_place_invalid_title_empty(self):

        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 400)

    #Testing latitude out of -90 and 90 range
    def test_create_place_invalid_title_latitude(self):

        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 92.292,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 400)

    #Testing latitude out of -180 and 180 range
    def test_create_place_invalid_title_longtitude(self):

        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.292,
            "longitude": -182.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 400)
    
    def test_get_all_places(self):
        place_response = self.client.get("/api/v1/places/")
        self.assertEqual(place_response.status_code, 200)

    def test_get_place_by_id(self):
        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        #Step 1 create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)

        place_id = place_response.get_json()['id']

        #Step 2 fetch place
        check_place = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(check_place.status_code, 200)

    def test_get_place_by_id(self):
        place_id = "invalid-id"

        check_place = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(check_place.status_code, 404)

    def test_update_place_data(self):
        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        #Step 1 create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)

        place_id = place_response.get_json()['id']

        new_title = uuid.uuid4().hex[:8]
        update_payload = {
            "title": f"new test titel {new_title}",
            "description": "New test description",
            "price": 200.0
        }

        update_place = self.client.put(f"/api/v1/places/{place_id}", json=update_payload)
        self.assertEqual(update_place.status_code, 200)

    #Test that payload should only include title, description, or price
    def test_update_place_invalid_data(self):
        user_id = self._seed_valid_place_dependencies()

        unique = uuid.uuid4().hex[:8]

        #Step 1 create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)

        place_id = place_response.get_json()['id']

        new_title = uuid.uuid4().hex[:8]
        update_payload = {
            "prices": 200.0
        }

        update_place = self.client.put(f"/api/v1/places/{place_id}", json=update_payload)
        self.assertEqual(update_place.status_code, 400)

    def test_get_place_reviews(self):
        user_id = self._seed_valid_place_dependencies()
        unique = uuid.uuid4().hex[:8]

        #Step 1 create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)

        place_id = place_response.get_json()['id']

        #Create multiple reviews
        for _ in range(10):
            review_user_id = self._seed_valid_place_dependencies()
            response = self.client.post('/api/v1/reviews/', json={
                "text": "Great place!",
                "rating": 5,
                "user_id": review_user_id,
                "place_id": place_id
            })
            self.assertEqual(response.status_code, 201)

        reviews = self.client.get(f"/api/v1/places/{place_id}/reviews")
        print(reviews)
        self.assertEqual(reviews.status_code, 200)

    def test_get_place_reviews_invalid_place_id(self):
        user_id = self._seed_valid_place_dependencies()
        unique = uuid.uuid4().hex[:8]

        #Step 1 create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {unique}",
            "description": "Place used only for review endpoint tests",
            "price": 100.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)

        place_id = place_response.get_json()['id']

        #Create multiple reviews
        for _ in range(10):
            review_user_id = self._seed_valid_place_dependencies()
            response = self.client.post('/api/v1/reviews/', json={
                "text": "Great place!",
                "rating": 5,
                "user_id": review_user_id,
                "place_id": place_id
            })
            self.assertEqual(response.status_code, 201)

        reviews = self.client.get(f"/api/v1/places/invalid-place/reviews")
        print(reviews)
        self.assertEqual(reviews.status_code, 404)
