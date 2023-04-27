from flask import request
from flask import Blueprint
from flask_jwt_extended import jwt_required

from helpers.response import api_response

book_api_blueprint = Blueprint("book_bp", __name__, url_prefix="/book")


@book_api_blueprint.route("/", methods=["GET"])
@jwt_required()
def list_books():
    from app import mongo

    db = mongo.db.books
    book_collection = db.find()

    book_list = []

    for el in book_collection:
        book_dict = {}
        for key, value in el.items():
            if isinstance(value, ObjectId):
                book_dict[key] = str(value)
            else:
                book_dict[key] = value
        book_list.append(book_dict)
    return api_response(200, message="Books retrieved successfully", data=book_list)


@book_api_blueprint.route("/<id>", methods=["GET"])
@jwt_required()
def get_book(id):
    db = mongo.db.books
    single_book = db.find_one({"_id": id})
    return api_response(200, data=single_book)


@book_api_blueprint.route("/", methods=["POST"])
@jwt_required()
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
    db.insert_one(
        {
            "title": title,
            "author": author,
            "description": description,
            "price": price,
        }
    )
    return api_response(201, "book added successfully")


@book_api_blueprint.route("/<id>", methods=["PUT"])
@jwt_required()
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
    db.update_one(
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
