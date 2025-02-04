#!/usr/bin/python3
"""Flask routes places"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_city(city_id):
    """return places in city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

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


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Search place"""
    query = request.get_json()
    if query is None:
        abort(400, "Not a JSON")

    if (query == {} or (
        not query.get('states')
            and not query.get('cities')
            and not query.get('amenities'))):
        places = []
        for place in list(storage.all(Place).values()):
            places.append(place.to_dict())
        return jsonify(places)

    places = []
    if query.get("states"):
        states = [storage.get(State, id) for id in query.get("states")]
        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if query.get("cities"):
        cities = [storage.get(City, id) for id in query.get("cities")]
        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if places == []:
        places = [place for place in storage.all(Place).values()]

    if query.get("amenities"):
        pass
    return jsonify([place.to_dict() for place in places])
