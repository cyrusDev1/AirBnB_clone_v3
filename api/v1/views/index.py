#!/usr/bin/python3
"""Flask routes"""
import imp
from flask import jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """Return status of api"""
    if request.method == 'GET':
        return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=['GET'])
def stats():
    """retrieves the number of each objects by type:"""
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"}
    stats = {}
    for key, value in classes.items():
        stats[value] = storage.count(key)
    return jsonify(stats)
