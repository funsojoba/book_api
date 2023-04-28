from flask import Blueprint

from flask import request
from bson import ObjectId

from helpers.response import api_response


user_blueprint = Blueprint("users", __name__, url_prefix="/user")


@user_blueprint.route("/", methods=["GET"])
def list_users():
    from app import mongo

    db = mongo.db.users

    users = db.find()
    user_list = []
    for user in users:
        user_dict = {}
        for key, value in user.items():
            if isinstance(value, ObjectId):
                user_dict[key] = str(value)
            else:
                user_dict[key] = value
        user_list.append(user_dict)
    return api_response(200, message="registered successfully", data=user_list)


@user_blueprint.route("/<id>", methods=["GET"])
def get_user(id):
    from app import mongo

    db = mongo.db.users

    single_user = db.find_one({"_id": id})
    return api_response(200, message="User retrieved successfully", data=single_user)
