from flask import Blueprint, jsonify
from buu import Building

api = Blueprint('Building API', __name__)
building = Building()

@api.route("/")
def index():
	return jsonify(building.getAll())