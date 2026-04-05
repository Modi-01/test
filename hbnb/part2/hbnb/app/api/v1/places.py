from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

@api.route("/")
class PlacesCollection(Resource):
    """
    GET /api/v1/places/
    Return list of all places
    """
    def get(self):
        places = facade.get_all_places()
        return [p.serializeList() for p in places], 200

    """
    POST /api/v1/places/
    Create a new place and attach to owner
    """
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = api.payload

        try:
            place = facade.create_place(data)
            
            return place.serializeNew(), 201
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "not found"}, 404
            return {"error": str(e)}, 400
        
       


@api.route("/<place_id>")
class PlaceResource(Resource):

    """
    GET /api/v1/places/<place_id>
    Return place by id
    """
    @api.response(200, 'Place found')
    @api.response(400, 'Invalid input data')
    def get(self, place_id):
        place = facade.get_place(place_id)

        if not place:
            return {"error": "place not found"}, 404
        
        return place.serializeById(), 200

    """
    PUT /api/v1/places/<place_id>
    Update place data
    """
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        data = api.payload
        if not isinstance(data, dict) or not data:
            return {"error", "Incorrect data passed."}
        
        required_fields = {"title", "description", "price"}
        has_extra = set(data.keys()) - required_fields

        if has_extra:
            return {"error": "You can only update title, description, or price"}, 400

        try:
            result = facade.update_place(place_id, data)
            return result, 200
        except ValueError as e:
            return {"error", str(e)}, 400
            
       
@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):

    """
    GET /api/v1/places/<place_id>/reviews
    Retrieve all reviews for a specific place
    """
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        try:
            reviews = facade.get_reviews_by_place(place_id)
            
            return [review.serializeList() for review in reviews], 200

        except ValueError as e:
            if "place not found" in str(e).lower():
                return {"error": "place not found"}, 404
            return {"error": str(e)}, 400
