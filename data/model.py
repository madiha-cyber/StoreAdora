"""Models from Myreens Beauty Hub"""

import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    # PK
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class UserProfile(db.Model):
    """Each user's profile"""

    __tablename__ = "UserProfile"

    # PK
    profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    insta_handle = db.Column(
        db.String,
        nullable=True,
    )
    bio = db.Column(
        db.String,
        nullable=True,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    youtube_handle = db.Column(
        db.String,
        nullable=True,
    )

    def __repr__(self):
        return f"<User user_id={self.profile_id} insta_handle={self.insta_handle}> user_id={self.user_id}"
