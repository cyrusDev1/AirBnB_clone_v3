from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'])
@app_views.route("/states/<state_id>", methods=['GET', 'DELETE'])
def states(state_id=''):
    """Retrieves the list of all State objects: GET /api/v1/states"""
    if state_id == '':
        if request.method == 'GET':
            all_states = []
            for state in list(storage.all(State).values()):
                all_states.append(state.to_dict())
            return jsonify(all_states)
    else:
        if request.method == 'GET':
            state = [state.to_dict() for state in list(storage.all(State).values()) if state.id == state_id]
            if len(state) == 0:
                abort(404)
            return jsonify(state[0])
        elif request.method == 'DELETE':
            state = [state for state in list(storage.all(State).values()) if state.id == state_id]
            if len(state) == 0:
                abort(404)
            storage.delete(state[0])
            storage.save()
            return jsonify({})
