#!/usr/bin/python3
"""Index module"""

from api.v1.views import app_views
from flask import jsonify

from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """Returns a JSON string"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """Returns a JSON string"""
    classes = {"amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User}
    for key, value in classes.items():
        classes[key] = storage.count(value)
    return jsonify(classes)
