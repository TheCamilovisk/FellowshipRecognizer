import imghdr
import os
from os import path
from flask import Flask, json, jsonify, request, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["MAX_CONTENT_LENGTH"] = 2097152  # 2 * 1024 * 1024
    app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]
    app.config["UPLOAD_PATH"] = "uploads"

    # Create the uploads folder, if necessary
    if not path.isdir(app.config["UPLOAD_PATH"]):
        os.makedirs(app.config["UPLOAD_PATH"])

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "File is too large"}), 413

    @app.route("/upload", methods=["POST"])
    def upload_files():
        uploaded_file = request.files["image"]
        filename = secure_filename(uploaded_file.filename)
        if filename != "":
            file_ext = path.splitext(filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(uploaded_file.stream):
                return jsonify({"error": "Invalid image"}), 400

            uploaded_file.save(path.join(app.config["UPLOAD_PATH"], filename))
        return jsonify({"img_id": filename}), 201

    return app
