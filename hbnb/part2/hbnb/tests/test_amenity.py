import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_by_id(self):

        # step 1 create an amenity
        payload = {
            "name": "Parking"
        }

        create_response = self.client.post('/api/v1/amenities/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        amenity_id = created_data['id']

        # step 2 retreive the amenity with id
        fetch_response = self.client.get(f"/api/v1/amenities/{amenity_id}")
        self.assertEqual(fetch_response.status_code, 200)

    def test_get_amenity_by_invalid_id(self):
        response = self.client.get('/api/v1/amenities/dd209f50-87c0-4eb5-848e-d2f01e5c650b')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):

        # step 1 create an amenity
        payload = {
            "name": "Pool"
        }

        create_response = self.client.post('/api/v1/amenities/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        amenity_id = created_data['id']

        update_payload = {
            "name": "Pool Updated"
        }

        # step 2 update the amenity with id
        fetch_response = self.client.put(f"/api/v1/amenities/{amenity_id}", json=update_payload)
        self.assertEqual(fetch_response.status_code, 200)

    def test_update_amenity_invalid_id(self):
        response = self.client.put('/api/v1/amenities/dd209f50-87c0-4eb5-848e-d2f01e5c650b', json={
            "name": "Gym"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_invalid_data(self):
        # step 1 create an amenity
        payload = {
            "name": "Breakfast"
        }

        create_response = self.client.post('/api/v1/amenities/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        amenity_id = created_data['id']

        update_payload = {
            "name": ""
        }

        # step 2 update the amenity with invalid data
        fetch_response = self.client.put(f"/api/v1/amenities/{amenity_id}", json=update_payload)
        self.assertEqual(fetch_response.status_code, 400)
