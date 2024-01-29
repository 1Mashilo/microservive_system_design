import jwt
import datetime
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import Flask, request, jsonify

from models import db  # Import SQLAlchemy instance from models.py

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Construct the database URL
quoted_password = quote_plus(os.getenv("POSTGRES_PASSWORD"))
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{quoted_password}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Configure Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



migrate = Migrate(app, db)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Import routes after initializing app and db
from routes import app_routes

# Register blueprints
app.register_blueprint(app_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

