#!/usr/bin/python3
"""Flask routes states"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'])
def state_cities(state_id=''):
    """Retrieves the list of all Cities related to a State objects:
    GET /api/v1/states/<state_id>/cities"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = list(map(lambda city: city.to_dict(), state.cities))
        return jsonify(cities)

    elif request.method == 'POST':
        req = request.get_json()

        if req is None:
            abort(400, "Not a JSON")
        if req.get("name") is None:
            abort(400, "Missing name")

        req.update({'state_id': state_id})
        new = City(**req)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'])
def city(city_id=''):
    """Retrieves a City object: GET /api/v1/cities/<city_id>"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    elif request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "PUT":
        req = request.get_json()

        if req is None:
            abort(400, "Not a JSON")
        city.my_update(req)
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({})
