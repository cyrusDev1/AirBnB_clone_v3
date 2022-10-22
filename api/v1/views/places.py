#!/usr/bin/python3
"""Flask routes places"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_city(city_id):
    """return places in city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(400)

    if request.method == 'GET':
        places = [
            place.to_dict() for place in list(storage.all(Place).values())
            if place.city_id == city_id
            ]
        return jsonify(places)

    elif request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        if req.get('user_id') is None:
            abort(400, "Missing user_id")
        if storage.get(User, req.get('user_id')) is None:
            abort(404)
        if req.get('name') is None:
            abort(400, "Missing name")
        req['city_id'] = city_id
        new = Place(**req)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places(place_id):
    """return place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        place.my_update(req)
        storage.save()
        return jsonify(place.to_dict()), 200
