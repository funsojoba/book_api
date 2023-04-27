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

from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

from helpers.response import api_response

from services.auth import auth_blueprint
from services.books_service import books_blueprint
from services.users import user_blueprint
from services.book_api_service import book_api_blueprint


# from services.users_service import users_blueprint


app = Flask(__name__)
app.secret_key = "secretkey"
app.config["JWT_SECRET_KEY"] = "secret-key"
jwt = JWTManager(app)

# Register the views Blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(book_api_blueprint)

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
    app.run(debug=True, port=6000)
    # host='0.0.0.0',
