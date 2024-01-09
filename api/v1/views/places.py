"""Creates a new view for Place objects that handles all
default RestFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request

from models import storage
from models.place import Place
from models.city import City

@app_views.route('/cities/<city_id>/places')
def places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>')
def place(place_id):
    """Retrieves a Place objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    place_dict = request.get_json()
    if place_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in place_dict:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, place_dict["user_id"])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if "name" not in place_dict:
        return jsonify({"error": "Missing name"}), 400
    place = Place(**place_dict)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    place_dict = request.get_json()
    if place_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in place_dict.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
