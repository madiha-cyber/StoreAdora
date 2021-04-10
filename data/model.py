"""Models for StoreAdora"""

from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

#
# Data Model for this file: https://dbdiagram.io/d/605d6433ecb54e10c33d565e
#


class User(db.Model):
    """
    A user
    """

    __tablename__ = "users"

    # Columns
    user_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, nullable=False
    )
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class UserProfile(db.Model):
    """Each user's profile"""

    __tablename__ = "userprofiles"

    # Relationships
    user = db.relationship("User", backref="userprofiles")

    # user_id is the primary key and foreign key
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), primary_key=True, nullable=False
    )
    profile_picture = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
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

    # user = db.relationship('User', backref=userprofile)
    # ^ what do you want to call 'users'?
    #                                ^ backref: what do you want 'user' to call you?
    # madiha = <User id=1 email='madiharules@gmail.com'>
    # madiha.??? < that's backref

    # last note about 1:1 https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#relationships-one-to-one
    # we also have to specify uselist=False as an option when calling db.relationship(uselist=False)

    def __repr__(self):
        return f"<UserProfile user_id={self.user_id} insta_handle={self.insta_handle} >"


class Post(db.Model):
    """A Post created by the user"""

    __tablename__ = "posts"

    # Relationships
    user = db.relationship("User", backref="posts")
    products = db.relationship("Product", backref="posts", secondary="postproducts")

    # Columns
    post_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, nullable=False
    )
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    post_description = db.Column(db.Text, nullable=True)
    makeup_type = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Post post_id={self.post_id} makeup_type={self.makeup_type}  post_description={self.post_description}"


class MakeupImage(db.Model):
    """Images of each post"""

    __tablename__ = "makeupimages"

    # Relationships
    post = db.relationship("Post", backref="makeupimages")

    # Columns
    img_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    image = db.Column(db.String)

    def __repr__(self):
        return f"<MakeupImage img_id={self.img_id} post_id={self.post_id}  image={self.image}"


class Favorite(db.Model):
    """Favorite Post of each User"""

    __tablename__ = "favorites"

    # Relationships
    post = db.relationship("Post", backref="favorites")
    user = db.relationship("User", backref="favorites")

    # Columns
    favorites_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    date_favorites = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Favorite favorites_id={self.favorites_id} user_id={self.user_id}  post_id={self.post_id} date_favorites={self.date_favorites}>"


#
@dataclass
class Product(db.Model):
    product_id: int
    title: str
    details: str
    url: str
    image: str

    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    details = db.Column(db.Text)
    url = db.Column(db.String)
    image = db.Column(db.String)

    def __repr__(self):
        return f"<Product product_id={self.product_id} details={self.details} url={self.url} image={self.image}>"


class PostProducts(db.Model):

    __tablename__ = "postproducts"

    # Columns
    post_product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))

    def __repr__(self):
        return f"<PostProducts post_product_id={self.post_product_id} product_id={self.product_id} post_id={self.post_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///finalproject", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
