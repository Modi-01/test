#!/usr/bin/python3
import unittest
import uuid
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ---------------------------------
    # Internal helpers (data setup only)
    # ---------------------------------
    def _seed_valid_review_dependencies(self):
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

        # create place (setup dependency only)
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

        return user_id, place_id

    def _create_review_for_test(self):
        user_id, place_id = self._seed_valid_review_dependencies()

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)
        return response.get_json()['id']

    # -----------------------------
    # Review endpoint tests only
    # -----------------------------
    def test_create_review(self):
        user_id, place_id = self._seed_valid_review_dependencies()

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing experience",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_data(self):
        
        user_id, _ = self._seed_valid_review_dependencies()

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Good",
            "rating": 4,
            "user_id": user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id(self):
        review_id = self._create_review_for_test()

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_invalid_id(self):
        response = self.client.get('/api/v1/reviews/dd209f50-87c0-4eb5-848e-d2f01e5c650b')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        review_id = self._create_review_for_test()

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review text",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)

    def test_update_review_invalid_id(self):
        response = self.client.put('/api/v1/reviews/dd209f50-87c0-4eb5-848e-d2f01e5c650b', json={
            "text": "Updated review text",
            "rating": 4
        })
        self.assertEqual(response.status_code, 404)

    def test_update_review_invalid_data(self):
        review_id = self._create_review_for_test()

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={})
        self.assertEqual(response.status_code, 400)

    def test_update_review_with_extra_fields(self):
        review_id = self._create_review_for_test()

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review text",
            "rating": 4,
            "user_id": "should-not-be-allowed"
        })
        self.assertEqual(response.status_code, 400)

    def test_delete_review(self):
        review_id = self._create_review_for_test()

        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_invalid_id(self):
        response = self.client.delete('/api/v1/reviews/dd209f50-87c0-4eb5-848e-d2f01e5c650b')
        self.assertEqual(response.status_code, 404)
