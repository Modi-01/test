#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
import re

api = Namespace("users", description="User operations")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route("/")
class UsersCollection(Resource):

    """
    GET /api/v1/users/
    Return list of all users
    """
    def get(self):
        users = facade.list_users()
        return [user.serialize() for user in users], 200


    """
    POST /api/v1/users/
    Register a new user
    """
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')

    def post(self):
        data = api.payload

        existing_user = facade.get_user_by_email(data['email'])
        if(existing_user):
            return { 'error': 'Email already registered'}, 400

        if not _EMAIL_RE.match(data['email']):
            return { 'error': 'Invalid input data.'}, 400
        
        try:
            user = facade.create_user(data)
            return user.serialize(), 201
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "user not found"}, 404
            return {"error": str(e)}, 400
        
@api.route("/<user_id>")
class UserResource(Resource):

    """
    GET /api/v1/users/<user_id>
    Return user by id  
    """
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "user not found"}, 404
        return user.serialize(), 200


    """
    PUT /api/v1/users/<user_id>
    Update user data (without password in response)
    """
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User Not Found')
    def put(self, user_id):
        data = api.payload
        
        required_fields = {"first_name", "last_name", "email"}
        has_extra = set(data.keys()) - required_fields

        if has_extra:
            return {"error": "You can only update first_name, last_name or price"}

        for key in required_fields:
            if(key == 'email'):
                if not _EMAIL_RE.match(data['email']):
                    return { 'error': 'Invalid input data.'}, 400
            
            if not isinstance(data.get(key), str) or not data.get(key).strip():
                return { 'error': 'Invalid input data' }, 400

        try:
            user = facade.update_user(user_id, data)
            return user.serialize(), 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "user not found"}, 404
            return {"error": str(e)}, 400
