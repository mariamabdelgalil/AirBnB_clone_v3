#!/usr/bin/python3
"""The users module"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """return all users information"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """return information about a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """create a new user"""
    json_body = request.get_json()
    if not json_body:
        abort(400, "Not a JSON")
    if 'email' not in json_body:
        abort(400, "Missing email")
    if 'password' not in json_body:
        abort(400, "Missing password")
    new_user = User(**json_body)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update an user"""
    user = storage.get(User, user_id)
    json_body = request.get_json()
    if not user:
        abort(404)
    if not json_body:
        abort(400, "Not a JSON")
    for key, value in json_body.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
