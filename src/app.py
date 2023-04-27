import jwt

import pymongo
import logging
from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
)
from werkzeug.security import check_password_hash

from helpers.response import api_response

from datetime import datetime, timedelta
from functools import wraps

from helpers.password_helper import password_regex

from werkzeug.security import generate_password_hash, check_password_hash

from services.auth import auth_blueprint

# from services.books import books_blueprint


app = Flask(__name__)
app.secret_key = "secretkey"
app.config["JWT_SECRET_KEY"] = "secret-key"
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint)
# app.register_blueprint(books_blueprint)
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


if __name__ == "__main__":
    app.run(debug=True)
    # host='0.0.0.0',
