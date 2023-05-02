import os
import jwt

import pymongo
import logging
from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

from helpers.response import api_response

from services.auth import auth_blueprint
from services.books_service import books_blueprint
from services.users import user_blueprint

from decouple import config

# from services.book_api_service import book_api_blueprint


# from services.users_service import users_blueprint


app = Flask(__name__)
app.secret_key = config("SECRET_KEY")
app.config["MONGO_URI"] = (
    "mongodb://"
    + config("MONGODB_USERNAME")
    + ":"
    + config("MONGODB_PASSWORD")
    + "@"
    + config("MONGODB_HOSTNAME")
    + ":27017/"
    + config("MONGODB_DATABASE")
)


def get_db():
    client = MongoClient(
        host="books_mongodb",
        port=27017,
        username="root",
        password="pass",
        authSource="admin",
    )
    db = client["books_db"]
    return db


# client = MongoClient(config('MONGO_URI'))
# db = client["book_api_db"]

app.config["JWT_SECRET_KEY"] = config("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Register the views Blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(books_blueprint)


mongo = PyMongo(app)


@app.route("/")
def index():
    return api_response(200, {"message": "Welcome to my API"})


if __name__ == "__main__":
    app.run(debug=True, port=6000)
    # host='0.0.0.0',
