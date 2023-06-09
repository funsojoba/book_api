from flask import request
from flask import Blueprint
from bson import ObjectId, json_util
from flask_jwt_extended import jwt_required, get_jwt_identity

from helpers.response import api_response

books_blueprint = Blueprint("books", __name__, url_prefix="/api/books")


@books_blueprint.route("/", methods=["GET"])
@jwt_required()
def list_books():
    from app import get_db

    db = get_db()
    book_collection = db.books.find()

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
    from app import get_db

    db = get_db()
    single_book = db.books.find_one({"_id": ObjectId(id)})

    if single_book:
        json_book = json_util.loads(json_util.dumps(single_book))

        json_book["_id"] = str(json_book["_id"])

        return api_response(
            200,
            data=json_book,
            message="Book retrieved successfully" if single_book else None,
        )
    else:
        return api_response(404, message="Book not found")


@books_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_book():
    from app import get_db

    db = get_db()

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

    book = db.books.insert_one(
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
    from app import get_db

    db = get_db()

    title = request.json.get("title", None)
    page_number = request.json.get("page_number", None)
    description = request.json.get("description", None)
    is_best_seller = request.json.get("is_best_seller", False)

    book = db.find_one({"_id": ObjectId(id)})

    db.books.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": title,
                "description": description,
            }
        },
    )
    return api_response(200, "book updated successfully")


@books_blueprint.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    from app import get_db

    db = get_db()

    db.books.delete_one({"_id": ObjectId(id)})
    return api_response(204, "book deleted successfully")
