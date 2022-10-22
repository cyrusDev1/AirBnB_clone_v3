#!/usr/bin/python3
"""Flask routes cities"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/cities", methods=['GET', 'POST'])
@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'])
def cities(city_id=''):
    """Retrieves the list of all City objects: GET /api/v1/cities"""
    if city_id == '':
        if request.method == 'GET':
            all_cities = []
            for city in list(storage.all(City).values()):
                all_cities.append(city.to_dict())
            return jsonify(all_cities)
        elif request.method == 'POST':
            req = request.get_json()
            if req is None:
                abort(400, "Not a JSON")
            if req.get("name") is None:
                abort(400, "Missing name")
            new = City(**req)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
    else:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(city.to_dict())
        elif request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return jsonify({})
        elif request.method == 'PUT':
            req = request.get_json()
            if req is None:
                abort(400, "Not a JSON")
            city.my_update(req)
            return jsonify(city.to_dict())
