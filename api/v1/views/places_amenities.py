#!/usr/bin/python3
"""Creates a new view for Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, request

from models import storage
from models.amenity import Amenity
from models.place import Place

@app_views.route('/places/<place_id>/amenities')
def amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                    methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """Deletes a Amenity objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity not in place.amenities:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                    methods=['POST'])
def create_amenity(place_id, amenity_id):
    """Creates a Amenity objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
