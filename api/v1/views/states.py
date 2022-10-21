#!/usr/bin/python3
"""Flask routes states"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'])
@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'])
def states(state_id=''):
    """Retrieves the list of all State objects: GET /api/v1/states"""
    if state_id == '':
        if request.method == 'GET':
            all_states = []
            for state in list(storage.all(State).values()):
                all_states.append(state.to_dict())
            return jsonify(all_states)
        elif request.method == 'POST':
            req = request.get_json()
            if req is None:
                abort(400, "Not a JSON")
            if req.get("name") is None:
                abort(400, "Missing name")
            new = State(**req)
            storage.new(new)
            storage.save()
            return make_response(jsonify(new.to_dict()), 201)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(state.to_dict())
        elif request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return jsonify({})
        elif request.method == 'PUT':
            req = request.get_json()
            if req is None:
                abort(400, "Not a JSON")
            state.update(req)
            return make_response(jsonify(state.to_dict()), 200)
