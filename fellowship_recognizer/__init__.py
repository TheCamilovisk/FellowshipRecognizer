from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=("GET",))
    def hello():
        return jsonify({"Hello": "World!!!"}), 200

    return app
