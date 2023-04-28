from flask import request
from flask import Blueprint
from bson import ObjectId, json_util
from flask_jwt_extended import jwt_required, get_jwt_identity

from helpers.response import api_response

books_blueprint = Blueprint("books", __name__, url_prefix="/book")


@books_blueprint.route("/", methods=["GET"])
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


@books_blueprint.route("/<id>", methods=["GET"])
@jwt_required()
def get_book(id):
    from app import mongo

    db = mongo.db.books
    single_book = db.find_one({"_id": ObjectId(id)})

    # Convert single_book to a JSON-compatible dictionary
    json_book = json_util.loads(json_util.dumps(single_book))

    # Replace ObjectId with its string representation
    json_book["_id"] = str(json_book["_id"])

    return api_response(
        200,
        data=json_book,
        message="Book retrieved successfully" if single_book else None,
    )


@books_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_book():
    from app import mongo

    db = mongo.db.books
    title = request.json.get("title", None)
    page_number = request.json.get("page_number", None)
    description = request.json.get("description", None)
    is_best_seller = request.json.get("is_best_seller", False)

    current_user_id = get_jwt_identity()

    errors = []

    if not title:
        errors.append("title is required")

    if not page_number:
        errors.append("page_number is required")

    if errors:
        return api_response(400, errors=errors)

    book = db.insert_one(
        {
            "title": title,
            "author": current_user_id,
            "description": description,
            "is_best_seller": is_best_seller,
        }
    )
    return api_response(201, "book added successfully")


@books_blueprint.route("/<id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    from app import mongo

    db = mongo.db.books
    title = request.json.get("title", None)
    page_number = request.json.get("page_number", None)
    description = request.json.get("description", None)
    is_best_seller = request.json.get("is_best_seller", False)

    book = db.find_one({"_id": ObjectId(id)})
    print("BOOK: ", book)

    db.update_one(
        {"_id": id},
        {
            "$set": {
                "title": title,
                "description": description,
            }
        },
    )
    return api_response(200, "book updated successfully")
