from api.v1.app import app_views
from flask import jsonify, request

from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews')
def reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>')
def review(review_id):
    """Retrieves a Review objects"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review objects"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a Review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    review_dict = request.get_json()
    if review_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in review_dict:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, review_dict["user_id"])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if "text" not in review_dict:
        return jsonify({"error": "Missing text"}), 400
    review = Review(**review_dict)
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    review_dict = request.get_json()
    if review_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in review_dict.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at",]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
