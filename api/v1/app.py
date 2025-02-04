#!/usr/bin/python3
"""Airbnb api with Flask"""
import os

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teawrdown(exc):
    """after each request, this method calls .close() on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle not found page"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    """Main flask app"""
    app.run(host=host, port=port)
