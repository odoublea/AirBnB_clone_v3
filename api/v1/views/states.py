from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State

@app_views.route('/states')
def states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states)

@app_views.route('/states/<state_id>')
def state(state_id):
    """Retrieves a State objects"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State objects"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State objects"""
    state_dict = request.get_json()
    if state_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in state_dict:
        return jsonify({"error": "Missing name"}), 400
    state = State(**state_dict)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    state_dict = request.get_json()
    if state_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in state_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
