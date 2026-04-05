from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
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
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = api.payload
        try:
            review = facade.create_review(data)
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
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        data = api.payload
        if not data:
            return {"error": "request body is required"}, 400
        
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
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "review not found"}, 404
            return {"error": str(e)}, 400
