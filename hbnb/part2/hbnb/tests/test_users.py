import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):

        # step 1 create a user
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe2@example.com"
        }

        create_response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        user_id = created_data['id']

        # step 2 retreive the user with id
        fetch_response = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(fetch_response.status_code, 200)


    def test_get_user_by_invalid_id(self):
        response = self.client.get('/api/v1/users/dd209f50-87c0-4eb5-848e-d2f01e5c650b')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):

        # step 1 create a user
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe3@example.com"
        }

        create_response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        user_id = created_data['id']

        update_payload = {
            "first_name": "Jane2",
            "last_name": "Doe2",
            "email": "jane.doe3@example1.com"
        }
        # step 2 update the user with id
        fetch_response = self.client.put(f"/api/v1/users/{user_id}", json=update_payload)
        self.assertEqual(fetch_response.status_code, 200)

    def test_update_user_invalid_id(self):
        response = self.client.put('/api/v1/users/dd209f50-87c0-4eb5-848e-d2f01e5c650b', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_user_invalid_email(self):
        # step 1 create a user
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe4@example.com"
        }

        create_response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        user_id = created_data['id']

        update_payload = {
            "first_name": "Jane2",
            "last_name": "Doe2",
            "email": "jane.doe3@example1,com"
        }
        # step 2 update the user with id
        fetch_response = self.client.put(f"/api/v1/users/{user_id}", json=update_payload)
        self.assertEqual(fetch_response.status_code, 400)

    def test_update_user_invalid_data(self):
        # step 1 create a user
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe5@example.com"
        }

        create_response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(create_response.status_code, 201)

        created_data = create_response.get_json()
        user_id = created_data['id']

        update_payload = {
            "first_name": "",
            "last_name": "Doe2",
            "email": "jane.doe3@example1,com"
        }
        # step 2 update the user with id
        fetch_response = self.client.put(f"/api/v1/users/{user_id}", json=update_payload)
        self.assertEqual(fetch_response.status_code, 400)
