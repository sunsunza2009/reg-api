from flask import Flask
from route import campus, building, room

app = Flask(__name__)
app.register_blueprint(campus.api,url_prefix="/api/campus")
app.register_blueprint(building.api,url_prefix="/api/building")
app.register_blueprint(room.api,url_prefix="/api/room")

if __name__ == '__main__':
	print(app.url_map)
	app.run()