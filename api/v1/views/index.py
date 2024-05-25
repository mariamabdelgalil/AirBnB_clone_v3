#!/usr/bin/python3
"""Views index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_route():
    """status route function: return OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats_route():
    """stats route function: return count of each class"""
    return jsonify({'amenities': storage.count("Amenity"),
                    'cities': storage.count("City"),
                    'places': storage.count("Place"),
                    'reviews': storage.count("Review"),
                    'states': storage.count("State"),
                    'users': storage.count("User")
                    })
