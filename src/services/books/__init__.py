from flask import Blueprint

books_blueprint = Blueprint("books", __name__)

from . import views
