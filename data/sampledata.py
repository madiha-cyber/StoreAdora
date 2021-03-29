import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from model import UserProfile, db
from crud import *

from datetime import datetime


def add_sample_data():

    users_list = []
    profiles_list = []
    posts_list = []
    favorites_list = []
    products_list = []

    # User 1
    u = create_user(email="madihagoheer@outlook.com", password="123")
    p = UserProfile(user_id=u.user_id, insta_handle="@madihagoheerofficial")
    users_list.append(u)
    profiles_list.append(p)

    # User 2
    u = create_user(email="asimgoheer@outlook.com", password="123")
    p = UserProfile(user_id=u.user_id, insta_handle="@asimgoheerofficial")
    users_list.append(u)
    profiles_list.append(p)

    # User 3
    u = create_user(email="myreen@hotmail.com", password="123")
    p = UserProfile(user_id=u.user_id, insta_handle="@myreengoheerofficial")
    users_list.append(u)
    profiles_list.append(p)

    # Product 1
    p = create_product("Foundation", "http://cnn.com", "/static/images/foundation1.jpg")
    products_list.append(p)

    # Product 1
    p = create_product("Mac Foundation 10", "http://cnn.com", "/static/images/foundation1.jpg")
    products_list.append(p)

    # User 1 Post 1
    p = create_post(user_id=users_list[0].user_id, post_description="This is a dummy post", makeup_type="Dramatic")
    posts_list.append(p)
    create_postproducts(products_list[0].product_id, p.post_id)

    # user 1 Post 2
    p = create_post(user_id=users_list[0].user_id, post_description="This is a dummy post 2", makeup_type="Classic")
    posts_list.append(p)
    create_postproducts(products_list[0].product_id, p.post_id)
    create_postproducts(products_list[1].product_id, p.post_id)

    # User 2 Favorites 1
    f = create_favorites(user_id=users_list[1].user_id, post_id=posts_list[0].post_id)
    favorites_list.append(f)

    # User 2 Favorites 2
    f = create_favorites(user_id=users_list[1].user_id, post_id=posts_list[1].post_id)
    favorites_list.append(f)

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
    connect_to_db(app)
    db.create_all()
    add_sample_data()
