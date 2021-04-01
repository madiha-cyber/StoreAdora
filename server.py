"""Server for StoreAdora app"""

from flask import Flask, render_template, request, flash, session, redirect
from data.model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage"""

    return render_template("homepage.html")


@app.route("/posts")
def get_all_posts():
    """View all posts"""

    posts = crud.get_posts()

    return render_template("all_posts.html", all_posts=posts)


@app.route("/posts/<post_id>")
def get_post(post_id):
    """View each post"""

    post = crud.get_post(post_id)
    products = crud.get_products_for_post(post_id)

    return render_template("post.details.html", post=post, products=products)


@app.route("/login", methods=["GET"])
def show_login():
    """Create a user"""
    return render_template("login_page.html")


@app.route("/login", methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email_and_password(email, password)
    if not user:
        flash("Invalid email/password")
    else:
        # Store user id in session or cookie
        return redirect("/user/" + str(user.user_id))


@app.route("/signup", methods=["GET"])
def show_signup():
    pass


@app.route("/signup", methods=["POST"])
def signup_user():
    pass


@app.route("/user/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    userprofile= get_user_profile(user_id)

    return render_template("user.html", user=user,
                                        userprofile=userprofile)


if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)
