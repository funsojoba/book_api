from flask import request
from flask import Blueprint
from flask_jwt_extended import jwt_required

from helpers.response import api_response

books_blueprint = Blueprint("book", __name__)


@books_blueprint.route("/", methods=["GET"])
@jwt_required
def list_books():
    db = mongo.db.books
    books_list = db.find()
    return api_response(200, data=books_list)


@books_blueprint.route("/<id>", methods=["GET"])
@jwt_required
def get_book(id):
    db = mongo.db.books
    book = db.find_one({"_id": id})
    return api_response(200, data=book)


@books_blueprint.route("/", methods=["POST"])
@jwt_required
def add_book():
    db = mongo.db.books
    title = request.json.get("title", None)
    author = request.json.get("author", None)
    description = request.json.get("description", None)
    price = request.json.get("price", None)
    if not title:
        return api_response(400, "title is required")
    if not author:
        return api_response(400, "author is required")
    if not description:
        return api_response(400, "description is required")
    if not price:
        return api_response(400, "price is required")
    book = db.insert_one(
        {
            "title": title,
            "author": author,
            "description": description,
            "price": price,
        }
    )
    return api_response(201, "book added successfully")


@books_blueprint.route("/<id>", methods=["PUT"])
@jwt_required
def update_book(id):
    db = mongo.db.books
    title = request.json.get("title", None)
    author = request.json.get("author", None)
    description = request.json.get("description", None)
    price = request.json.get("price", None)
    if not title:
        return api_response(400, "title is required")
    if not author:
        return api_response(400, "author is required")
    if not description:
        return api_response(400, "description is required")
    if not price:
        return api_response(400, "price is required")
    book = db.update_one(
        {"_id": id},
        {
            "$set": {
                "title": title,
                "author": author,
                "description": description,
                "price": price,
            }
        },
    )
    return api_response(200, "book updated successfully")
