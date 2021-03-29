"""Models from Myreens Beauty Hub"""

import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

#
# Data Model for this file: https://dbdiagram.io/d/605d6433ecb54e10c33d565e
#


class User(db.Model):
    """A user."""

    __tablename__ = "user"

    # PK
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class UserProfile(db.Model):
    """Each user's profile"""

    __tablename__ = "userprofile"

    # PK
    profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # FK
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    insta_handle = db.Column(
        db.String,
        nullable=True,
    )
    bio = db.Column(
        db.String,
        nullable=True,
    )
    youtube_handle = db.Column(
        db.String,
        nullable=True,
    )

    def __repr__(self):
        return f"<UserProfile profile_id={self.profile_id} insta_handle={self.insta_handle} >"


class Post(db.Model):
    """A Post created by the user"""

    __tablename__ = "post"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    post_description = db.Column(db.Text, nullable=True)
    makeup_type = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Post post_id={self.post_id} makeup_type={self.makeup_type}  post_description={self.post_description}"


class MakeupImage(db.Model):
    """Images of each post"""

    __tablename__ = "makeupimage"

    img_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"))
    img_url = db.Column(db.String)

    def __repr__(self):
        return f"<MakeupImage img_id={self.img_id} post_id={self.post_id}  img_url={self.img_url}"


class Favorites(db.Model):
    """Favorites Post of each User"""

    __tablename__ = "favorites"

    favorites_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"))
    date_favorites = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Favorites favorites_id={self.favorites_id} user_id={self.user_id}  post_id={self.post_id} date_favorites={self.date_favorites}>"


class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_details = db.Column(db.Text)
    website_link = db.Column(db.String)
    image_url = db.Column(db.String)

    def __repr__(self):
        return f"<Product product_id={self.product_id} product_details={self.product_details} website_link={self.website_link} img_url={self.img_url}>"


class PostProducts(db.Model):

    __tablename__ = "postproducts"

    post_product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"))

    def __repr__(self):
        return f"<PostProducts post_product_id={self.post_product_id} product_id={self.product_id} post_id={self.post_id}>"
