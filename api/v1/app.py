#!/usr/bin/python3
"""Airbnb api with Flask"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

app.url_map.strict_slashes = False

HBNB_API_HOST = "0.0.0.0"
HBNB_API_PORT = 5000


@app.teardown_appcontext
def teawrdown(exc):
    """after each request, this method calls .close() on
    the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    """Main flask app"""
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT)
