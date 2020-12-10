from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """ User model """

    # By default SQLAlchemy defines the table as the lowercase version of the class: User --> user
    # We can define the name of the table ourselves:
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
