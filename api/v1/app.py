#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS, cross_origin
from models import storage
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')

cors = CORS(app, resources={r"/*": {"origins": host}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


if __name__ == '__main__':
    """
    MAIN Flask App
    """
    app.run(host=host, port=port, threaded=True)
