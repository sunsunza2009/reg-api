from flask import Blueprint, jsonify
from buu import Campus

api = Blueprint('Campus API', __name__)

@api.route("/")
def index():
	return jsonify(Campus.getAll())