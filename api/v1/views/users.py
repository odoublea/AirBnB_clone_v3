""" Creates a new view for User objects that handles all
default RestFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request

from models import storage
from models.user import User

@app_views.route('/users')
def users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users/<user_id>')
def user(user_id):
    """Retrieves a User objects"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User objects"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User objects"""
    user_dict = request.get_json()
    if user_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in user_dict:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in user_dict:
        return jsonify({"error": "Missing password"}), 400
    user = User(**user_dict)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    user_dict = request.get_json()
    if user_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in user_dict.items():
        if key not in ["id", "email", "created_at", "updated_at",]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
