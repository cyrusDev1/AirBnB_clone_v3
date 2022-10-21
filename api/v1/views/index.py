#!/usr/bin/python3
"""Flask routes"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=['GET'])
def status():
    """Return status of api"""
    return jsonify({'status': 'OK'})
