#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
HOST = '0.0.0.0'
PORT = '5000'


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """Close storage in when flask app finish its process"""
    storage.close()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
