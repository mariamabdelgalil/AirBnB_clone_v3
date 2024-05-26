#!/usr/bin/python3
"""The states module"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """return all cities information in a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_arr = []
    for city in cities:
        cities_arr.append(city.to_dict())
    return jsonify(cities_arr)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """return information about a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city by its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new state"""
    state = storage.get(State, state_id)
    json_body = request.get_json()
    if not state:
        abort(404)
    if not json_body:
        abort(400, "Not a JSON")
    if 'name' not in json_body:
        abort(400, "Missing name")
    json_body['state_id'] = state_id
    new_city = City(**json_body)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update an state"""
    city = storage.get(City, city_id)
    json_body = request.get_json()
    if not city:
        abort(404)
    if not json_body:
        abort(400, "Not a JSON")
    for key, value in json_body.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
