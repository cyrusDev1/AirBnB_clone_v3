#!/usr/bin/python3
"""Flask routes for users"""
from email.policy import strict

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users(user_id=''):
    """Return users with jsonfy"""
    if user_id == '':
        if request.method == 'GET':
            all_users = []
            for user in list(storage.all(User).values()):
                all_users.append(user.to_dict())
            return jsonify(all_users)
        elif request.method == 'POST':
            req = request.get_json()
            if req is None:
                abort(400, "Not a JSON")
            for key in ['email', 'password']:
                if req.get(key) is None:
                    abort(400, "Missing {}".format(key))
            new = User(**req)
            storage.new(new)
            storage.save()
            return make_response(jsonify(new.to_dict()), 201)
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(user.to_dict())
        elif request.method == 'DELETE':
            storage.delete(user)
            storage.save()
            return make_response(jsonify({}), 200)
        elif request.method == 'PUT':
            req = request.get_json()
            if req is None:
                abort(400, "Not a JSON")
            user.my_update(req)
            return make_response(jsonify(user.to_dict()), 200)
