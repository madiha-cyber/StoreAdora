"""Server for StoreAdora app"""

from flask import Flask, render_template, request, flash, session, redirect
from data.model import connect_to_db
import os
import crud

from jinja2 import StrictUndefined
from PIL import Image

app = Flask(__name__, static_url_path="/static")
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
    post_images = crud.get_post_images(post_id)

    return render_template(
        "post.details.html", post=post, products=products, post_images=post_images
    )


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

    if "user_id" not in session and not session["user_id"]:
        return redirect("/")

    user_id = session["user_id"]

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)

    return render_template("profile.html", user=user, userprofile=userprofile)


@app.route("/profile/edit", methods=["GET"])
def start_edit_profile():

    if "user_id" not in session and not session["user_id"]:
        return redirect("/")

    user_id = session["user_id"]

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)

    return render_template("edit_profile.html", user=user, userprofile=userprofile)


UPLOAD_FOLDER = "./static/images/profile/"


@app.route("/profile/edit", methods=["POST"])
def save_edit_profile():

    if "user_id" not in session and not session["user_id"]:
        return redirect("/")

    user_id = session["user_id"]

    form_id = request.form.get("form_id")
    if form_id == "basic_info":
        user_id = session["user_id"]
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        insta_handle = request.form.get("insta_handle")
        bio = request.form.get("bio")
        return redirect("/profile")
    elif form_id == "profile_picture":
        if "file1" not in request.files:
            flash("No Profile Picture found")
            return redirect("/profile")

        f = request.files["file1"]

        # if len(f.stream) > 3000000:
        #     flash("file too big")
        #     return redirect("/profile")

        img = Image.open(f.stream)
        if img.format != "JPEG":
            flash("No Profile Picture found")
            return redirect("/profile")

        original_size = img.size
        if original_size[0] > 5000 or original_size[0] < 50:
            flash("No Profile Picture found")
            return redirect("/profile")

        if original_size[1] > 5000 or original_size[1] < 50:
            flash("No Profile Picture found")
            return redirect("/profile")
        smallest_side = min(original_size[0], original_size[1])
        if original_size[0] > original_size[1]:
            x = (original_size[0] - smallest_side) / 2
            new_size = (x, 0, x + smallest_side, original_size[1])
        elif original_size[0] < original_size[1]:
            y = (original_size[1] - smallest_side) / 2
            new_size = (0, y, smallest_side, y + smallest_side)
        else:
            new_size = (0, 0, smallest_side, smallest_side)

        cropped_image = img.crop(new_size)
        resize_image = cropped_image.resize((100, 100))

        file_name = str(user_id) + ".jpg"
        path = os.path.join(UPLOAD_FOLDER, file_name)
        resize_image.save(path)

        crud.set_user_profile_picture(user_id, file_name)

        flash("Uploaded picture")
        return redirect("/profile")
    else:
        return redirect("/profile")

    # Update user profile to reflect these new changes.


@app.route("/newlook")
def show_newlook_page():
    # Show newlook page
    return render_template("newlook.html")


if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)
