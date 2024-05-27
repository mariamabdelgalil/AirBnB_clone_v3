#!/usr/bin/python3
"""The places_amenities module"""
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """Return all place amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """Delete an amenity of a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for existing_amenity in place.amenities:
        if existing_amenity.id == amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity_id)
            storage.save()
            return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Add a new amenity to a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict())
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
