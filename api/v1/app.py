#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
HOST = getenv("HBNB_API_HOST") or '0.0.0.0'
PORT = getenv("HBNB_API_PORT") or '5000'


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """Close storage in when flask app finish its process"""
    storage.close()

@app.errorhandler(404)
def not_found(e):
    """Handle 404 not found page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(404)
def not_found(e):
    """Handle 404 not found page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)
