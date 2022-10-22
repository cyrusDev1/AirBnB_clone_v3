#!/usr/bin/python3
"""Flask routes states"""
from flask import abort, jsonify, make_response, request
from requests import delete

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'])
def index():
    """Retrieves the list of all Amenities objects: GET /api/v1/amenities"""

    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route("/amenities", methods=['POST'])
def create():
    """Creates a Amenity: POST /api/v1/amenities"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if req.get("name") is None:
        abort(400, "Missing name")

    new = Amenity(**req)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def show(amenity_id):
    """Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update(amenity_id):
    """Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    req = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if req is None:
        abort(400, "Not a JSON")
    amenity.my_update(req)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def destroy(amenity_id):
    """Deletes a Amenity object: DELETE /api/v1/amenities/<amenity_id>"""

    storage.delete(amenity_id)
    storage.save()
    return jsonify({})
