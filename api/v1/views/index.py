#!/usr/bin/python3
"""Views index module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status_route():
    """status route function: return OK"""
    return jsonify({'status': 'OK'})