from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("reviews", description="Review operations")

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route("/")
class ReviewsCollection(Resource):

    """
    GET /api/v1/reviews/
    Return a list of all reviews
    """
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        reviews = facade.get_all_reviews()
        return [r.serializeList() for r in reviews], 200

    """
    POST /api/v1/reviews/
    Create a new review
    """
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = api.payload
        current_user = get_jwt_identity()

        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Incorrect place id.'}, 404
        
        if place.owner.id == current_user:
            return {'error': 'You cannot review your own place.'}, 400
    
        user_already_reviewed = any(review.author.id == current_user for review in place.reviews)
        if user_already_reviewed:
            return {'error': 'You have already reviewed this place.'}, 400

        try:
            review = facade.create_review(current_user, data)
            return review.serialize(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<review_id>")
class ReviewResource(Resource):

    """
    GET /api/v1/reviews/<review_id>
    Return review by id
    """
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "review not found"}, 404
        
        return review.serialize(), 200

    """
    PUT /api/v1/reviews/<review_id>
    Update review 
    """
    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        data = api.payload
        current_user = get_jwt_identity()
        if not data:
            return {"error": "request body is required"}, 400
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Couldn't locate review."}, 404
        
        if review.author.id != current_user:
            return {"error": "Unauthorized action."}, 403

        required_fields = {"text", "rating"}
        has_extra = set(data.keys()) - required_fields

        if has_extra:
            return {"error": "You can only update text or rating"}, 400

        try:
            review = facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "review not found"}, 404
            return {"error": str(e)}, 400


    """
    DELETE /api/v1/reviews/<review_id>
    Update review 
    """
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        current_user = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Couldn't locate review."}, 404
        
        if review.author.id != current_user:
            return {"error": "Unauthorized action."}, 403
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "review not found"}, 404
            return {"error": str(e)}, 400
