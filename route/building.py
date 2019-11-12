from flask import Blueprint, jsonify
from buu import Building

api = Blueprint('Building API', __name__)
building = Building()

@api.route("/")
def index():
	try:
		return jsonify(building.getAll())
	except Exception as e:
		return jsonify({"error": str(e)}), 500