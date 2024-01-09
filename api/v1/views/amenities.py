"""Amenity objects that handles all default 
RestFul API actions""
"""
from api.v1.views import app_views
from flask import jsonify, request

from models import storage
from models.amenity import Amenity

@app_views.route('/amenities')
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>')
def amenity(amenity_id):
    """Retrieves a Amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a Amenity objects"""
    amenity_dict = request.get_json()
    if amenity_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in amenity_dict:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**amenity_dict)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    amenity_dict = request.get_json()
    if amenity_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in amenity_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
