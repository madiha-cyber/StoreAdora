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
    """Show Login page"""

    # Check if session exists.
    # If session exists redirect to /profile
    if "user_id" in session and session["user_id"]:
        # session['u#ser_id'] = user.user_id
        # Assigning value of user_id at key session['user_id'] to id
        id = session["user_id"]
        return redirect("/profile")

    # If session does not exists display login page
    return render_template("login_page.html")


@app.route("/login", methods=["POST"])
def login_user():
    # Login the user and redirect to /profile page

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email_and_password(email, password)
    print("*********************")
    print(user)
    if not user:
        flash("Invalid email/password")
    else:
        session["user_id"] = user.user_id
        return redirect("/profile")


@app.route("/logout", methods=["GET"])
def logout_user():
    """logout the user"""

    if "user_id" in session and session["user_id"]:
        del session["user_id"]

    return redirect("/")


@app.route("/signup", methods=["GET"])
def show_signup():
    # Show Signup page
    if "user_id" in session and session["user_id"]:
        # flash("You are already logged In")
        return redirect("/")
    else:
        return render_template("sign_up.html")


@app.route("/signup", methods=["POST"])
def signup_user():
    # Create new Account then redirect to /profile page

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("You already have an account with this email")
        return redirect("/signup")
    else:
        user = crud.create_user_and_profile(fname, lname, email, password)
        session["user_id"] = user.user_id
        return redirect("/profile")


@app.route("/user/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)

    return render_template("user_profile.html", user=user, userprofile=userprofile)


@app.route("/profile")
def show_userprofile():
    """Home page for logged in user."""

    if not session["user_id"] or not session["user_id"]:
        return redirect("/")

    user_id = session["user_id"]

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)

    return render_template("profile.html", user=user, userprofile=userprofile)


@app.route("/profile/edit", methods=["GET"])
def start_edit_profile():

    if not session["user_id"] or not session["user_id"]:
        return redirect("/")

    user_id = session["user_id"]

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)

    return render_template("edit_profile.html", user=user, userprofile=userprofile)


@app.route("/profile/edit", methods=["POST"])
def save_edit_profile():

    if not session["user_id"] or not session["user_id"]:
        return redirect("/")

    user_id = session["user_id"]
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    # Update user profile to reflect these new changes.


@app.route("/newlook")
def show_newlook_page():
    # Show newlook page
    return render_template("newlook.html")


if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)
