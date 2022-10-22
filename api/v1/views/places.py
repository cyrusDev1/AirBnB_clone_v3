#!/usr/bin/python3
"""Flask routes places"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities')
def cities():
    all_cities = []
    for user in list(storage.all(City).values()):
        all_cities.append(user.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>/places')
def places_city(city_id=""):
    """return places in city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(400)
    places = [
        place.to_dict() for place in list(storage.all(Place).values())
        if place.city_id == city_id
        ]
    return jsonify(places)


@app_views.route('/places/<place_id>')
def places_index(place_id='', methods=['GET']):
    """return place"""
    place = storage.get(Place, place_id)
    if city is None:
        abort(400)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
            for key in ['user_id', 'name']:
                if req.get(key) is None:
                    abort(400, "Missing {}".format(key))
            user = storage.get(User, user_id)
            if user is None:
                abort(404)
            new = Place(**req)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>')
def places_index(place_id='', methods=['GET', 'DELETE', 'PUT']):
    """return place"""
    place = storage.get(Place, place_id)
    if city is None:
        abort(400)
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
        return jsonify(place.to_dict())
