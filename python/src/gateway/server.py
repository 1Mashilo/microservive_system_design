import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo 
from auth import validate
from auth_svc import access 
from storage import util

# Initialize Flask app
server = Flask(__name__)

# Configure MongoDB connection URI
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

# Initialize PyMongo to connect to MongoDB
mongo = PyMongo(server)

# Initialize GridFS for file storage
fs = gridfs.GridFS(mongo.db)

# Configure RabbitMQ connection
params = pika.URLParameters('rbbitmq_url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Route for user login
@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err, 401

# Route for file upload
@server.route("/upload", methods=["POST"])
def upload():
    # Validate user token
    access, err = validate.token(request)
    access, err = json.loads(access)

    if access["admin"]:
        if len(request.files) != 1:
            return "Exactly 1 file required", 400

    for _, f in request.files.items():
        err = util.upload(f, fs, channel, access)
        if err:
            return err, 401

    return "Success!", 200

# Route for file download - Needs implementation
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(debug=True)
