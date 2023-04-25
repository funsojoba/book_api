import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __repr__(self):
        return f"{self.username}"
    
    
class Book(db.Model):
    id = db.column(db.String(50), primary_key=True, default=uuid.uuid4)
    author = db.Column(db.String(100), db.ForeignKey("User.id"), nullable=False)
    page_numbers = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    is_best_seller = db.Column(db.Boolean(), nullable=False)


