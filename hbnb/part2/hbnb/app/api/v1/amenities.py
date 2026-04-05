#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace("amenities", description="Amenity operations")

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route("/")
class AmenitiesCollection(Resource):

    """
    GET /api/v1/amenities/
    Return list of amenities
    """
    @api.response(200, 'List all amenities')
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.serialize() for a in amenities], 200


    """
    POST /api/v1/amenities/
    Creatre a new amenity 
    """
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = api.payload
        if not isinstance(data.get('name'), str) or not data.get('name'):
            return { "error": "Amenity name is required and must be a string."}, 400
    
        amenity = facade.create_amenity(data)

        return amenity.serialize(), 201

@api.route("/<amenity_id>")
class AmenityItem(Resource):

    """
    GET /api/v1/amenities/<amenity_id>
    Get amenity by id
    """
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "amenity not found"}, 404
        
        return amenity.serialize(), 200

    """
    PUT /api/v1/amenities/<amenity_id>
    Update amenity
    """
    def put(self, amenity_id):
        data = api.payload
        
        if not isinstance(data.get('name'), str) or not data.get('name'):
            return { "error": "Amenity name is required and must be a string."}, 400
        try:
            amenity = facade.update_amenity(amenity_id, data)
            return amenity.serialize(), 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "user not found"}, 404
            return {"error": str(e)}, 400
