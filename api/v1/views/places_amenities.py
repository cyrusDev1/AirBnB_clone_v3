#!/usr/bin/python3
"""Flask routes states"""
from flask import abort, jsonify, make_response, request
import os
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity


HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenites(place_id):
    """Return amenites of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    if HBNB_TYPE_STORAGE == 'db':
        amenities = list(
            map(lambda amenity: amenity.to_dict(), place.amenities))
    else:
        amenity_ids = place.amenity_ids
        for amenity_id in amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is not None:
                amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=[
    'DELETE'])
def destroy_amenities(place_id, amenity_id):
    """Destroy an amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if HBNB_TYPE_STORAGE == 'db':
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenities(place_id, amenity_id):
    """Link an amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if HBNB_TYPE_STORAGE == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
