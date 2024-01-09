"""Flask application set up"""""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
    
if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
