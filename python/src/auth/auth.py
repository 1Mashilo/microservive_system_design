import psycopg2
import jwt
import datetime
import os
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return jsonify({"message": "Missing credentials"}), 401

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

    cur = conn.cursor()
    cur.execute("SELECT email, password FROM users WHERE email=%s", (auth.username,))
    user_row = cur.fetchone()

    if user_row:
        email, password = user_row[0], user_row[1]

        if auth.username != email or auth.password != password:
            return jsonify({"message": "Invalid credentials"}), 401
        else:
            token = create_jwt(auth.username, os.getenv("JWT_SECRET"), True)
            return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers.get("Authorization")

    if not encoded_jwt:
        return jsonify({"message": "Missing credentials"}), 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return jsonify(decoded), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Not authorized"}), 403

def create_jwt(username, secret_key, authz):
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    payload = {
        "username": username,
        "exp": expiration_time,
        "admin": authz,
    }
    return jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")
