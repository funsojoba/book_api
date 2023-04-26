import jwt

import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash

from helpers.response import api_response

from datetime import datetime, timedelta
from functools import wraps

from helpers.password_helper import password_regex

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "secretkey"
app.config["JWT_SECRET_KEY"] = "secret-key"
jwt = JWTManager(app)
# api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/book_api_db"
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'book_api_db',
#     'host': 'localhost',
#     'port': 27017
# }

# my_client = pymongo.MongoClient("mongodb://localhost:27017/")
# my_db = my_client["book_api_db"]


mongo = PyMongo(app)


@app.route("/")
def index():
    return api_response(200, {"message": "Welcome to my API"})


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Not Found: " + request.url,
    }
    response = jsonify(message)
    response.status_code = 404

    return response


@app.route("/user/signup/", methods=["POST"])
def signup():
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
        return api_response(errors, 400)

    if request.method == "POST":
        hashed_password = generate_password_hash(password)

        id = db.insert_one(
            {"email": email, "password": hashed_password, "username": username}
        )
        return api_response("registered successfully", 201)
    else:
        return not_found()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/user/login/", methods=["POST"])
def login():
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


@app.route("/users", methods=["GET"])
def users():
    db = mongo.db.users
    output = []

    for q in db.find():
        output.append(
            {"id": dumps(q["_id"]), "email": q["email"], "username": q["username"]}
        )

    return api_response(200, "success", output)


if __name__ == "__main__":
    app.run(debug=True)
    # host='0.0.0.0',
