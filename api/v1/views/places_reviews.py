#!/usr/bin/python3
"""Flask routes states"""
from flask import abort, jsonify, make_response, request
from requests import delete

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("places/<place_id>/reviews", methods=['GET'])
def places_reviews(place_id):
    """Retrieves the list of all Review objects of a
    Place: GET /api/v1/places/<place_id>/reviews"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = list(map(lambda review: review.to_dict(), place.reviews))
    return jsonify(reviews)


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def create_review(place_id):
    """Creates a Review: POST /api/v1/places/<place_id>/reviews"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    if req.get("user_id") is None:
        abort(400, "Missing user_id")

    if storage.get(User, req.get("user_id")) is None:
        abort(404)

    if req.get("text") is None:
        abort(400, "Missing text")

    req.update({'place_id': place_id})
    new = Review(**req)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['GET'])
def show_review(review_id):
    """Retrieves a Review object: GET /api/v1/reviews/<review_id>"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_review(review_id):
    """Updates a Review object: PUT /api/v1/reviews/<review_id>"""
    req = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if req is None:
        abort(400, "Not a JSON")
    review.my_update(req)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def destroy_review(review_id):
    """Deletes a Review object: DELETE /api/v1/reviews/<review_id>"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({})
