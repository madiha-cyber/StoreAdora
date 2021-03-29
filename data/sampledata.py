import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from model import User, UserProfile, db

from datetime import datetime


def add_sample_data():

    users_list = []
    profiles_list = []

    # User 1
    u = User(email="madihagoheer@outlook.com", password="123")
    p = UserProfile(user_id=u.user_id, insta_handle="@madihagoheerofficial")
    users_list.append(u)
    profiles_list.append(p)

    # User 2
    u = User(email="asimgoheer@outlook.com", password="123")
    p = UserProfile(user_id=u.user_id, insta_handle="@asimgoheerofficial")
    users_list.append(u)
    profiles_list.append(p)

    # Add all the objects to the db
    db.session.add_all(users_list)
    db.session.add_all(profiles_list)
    print("Added objects to DB")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///finalproject"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")



if __name__ == "__main__":
    from flask import Flask

    os.system("dropdb finalproject")
    os.system("createdb finalproject")

    app = Flask(__name__)
    connect_to_db(app
    )
    db.create_all()
    add_sample_data()