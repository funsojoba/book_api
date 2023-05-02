from flask import Blueprint

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
)

from helpers.response import api_response
from helpers.password_helper import password_regex


auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_blueprint.route("/signup/", methods=["POST"])
def signup():
    from app import mongo

    db = mongo.db.users
    errors = []
    username = request.json.get("username", None)
    if not username:
        errors.append("Username is required")

    email = request.json.get("email", None)
    if not email:
        errors.append("Email is required")

    password = request.json.get("password", None)
    if not password:
        errors.append("Password is required")

    if not password_regex(password):
        errors.append(
            "Password must be between 6 and 12 characters with at least, one uppercase and one lowercase letter"
        )

    if len(username) < 4 or len(username) > 10:
        errors.append("username must be between 4 and 10 characters")

    # check if username or email already exists
    if db.find_one({"username": username}) or db.find_one({"email": email}):
        errors.append("username or email already exists")

    if errors:
        return api_response(400, errors=errors)

    hashed_password = generate_password_hash(password)

    id = db.insert_one(
        {"email": email, "password": hashed_password, "username": username}
    )
    return api_response(201, "registered successfully")


@auth_blueprint.route("/login/", methods=["POST"])
def login():
    from app import mongo

    db = mongo.db.users
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    username_or_email = username or email

    errors = []

    if not username_or_email:
        errors.append("Username or email is required")

    if not password:
        errors.append("Password is required")

    if errors:
        return api_response(400, errors=errors)

    user = db.find_one(
        {"$or": [{"username": username_or_email}, {"email": username_or_email}]}
    )

    if user and check_password_hash(user["password"], password):
        access_token = create_access_token(identity=str(user["_id"]))
        return api_response(
            200, "Logged in successfully", {"access_token": access_token}
        )
    return api_response(401, "Invalid username/email or password")
