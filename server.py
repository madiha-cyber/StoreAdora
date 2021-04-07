"""Server for StoreAdora app"""

from flask import Flask, render_template, request, flash, session, redirect
from data.model import connect_to_db
import os
import crud

from jinja2 import StrictUndefined
from PIL import Image
import image_helpers

app = Flask(__name__, static_url_path="/static")
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER_PROFILE_PICTURE = "./static/images/profile/"
UPLOAD_FOLDER_POST_PICTURES = "./static/images/posts/"


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


def is_user_signed_in():
    """
    Check if user's session exists
    """
    # return "user_id" in session and session["user_id"] != None
    return session.get("user_id") != None


@app.route("/login", methods=["GET"])
def show_login_page():
    """
    Show Login page
    """

    # Check User Logged In
    if is_user_signed_in():
        return redirect("/profile")

    # If session does not exists display login page
    return render_template("login_page.html")


@app.route("/login", methods=["POST"])
def login_user():
    """
    Login the user and redirect to /profile page
    """

    # Check User Logged In
    if is_user_signed_in():
        return redirect("/profile")

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email_and_password(email, password)
    if not user:
        flash("Invalid email/password")
        return redirect("/login")
    else:
        session["user_id"] = user.user_id
        return redirect("/profile")


@app.route("/logout", methods=["GET"])
def logout_user():
    """
    logout the user
    """
    # Check User Logged In
    if is_user_signed_in():
        del session["user_id"]
    return redirect("/")


@app.route("/signup", methods=["GET"])
def show_signup_page():
    """
    Show Signup page
    """
    # Check User Logged In
    if is_user_signed_in():
        return redirect("/")
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_user():
    """
    Create new Account then redirect to /profile page
    """
    # Check User Logged In
    if is_user_signed_in():
        return redirect("/")

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Make sure we don't allow same email again.
    existing_user = crud.get_user_by_email(email)

    if existing_user:
        flash("This email is already in use.")
        return redirect("/signup")
    else:
        # create a new user and store its value in the session
        user = crud.create_user_and_profile(first_name, last_name, email, password)
        session["user_id"] = user.user_id
        return redirect("/profile")


@app.route("/user/<user_id>")
def show_user(user_id):
    """
    Show details on a particular user.
    """
    user = crud.get_user_by_id(user_id)
    if not user:
        return render_template("user_profile_not_found.html")

    userprofile = crud.get_user_profile(user_id)
    return render_template("user_profile.html", user=user, userprofile=userprofile)


@app.route("/profile", methods=["GET"])
def show_userprofile():
    """
    Home page for logged in user.
    """
    # Check User Logged In
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)
    user_posts = crud.get_posts_for_user(user_id)

    return render_template(
        "profile.html", user=user, userprofile=userprofile, user_posts=user_posts
    )


@app.route("/profile/edit", methods=["GET"])
def show_edit_profile_page():
    """
    Show edit profile page.
    """
    # Check User Logged In
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)
    return render_template("edit_profile.html", user=user, userprofile=userprofile)


@app.route("/profile/edit", methods=["POST"])
def save_edit_profile():
    """
    Save edit profile changes
    """
    # Check User Logged In
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]
    form_id = request.form.get("form_id")
    # If we are updating basic_info section
    if form_id == "basic_info":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        insta_handle = request.form.get("insta_handle")
        bio = request.form.get("bio")
        # Add this to database
        # Missing
        crud.update_user_profile_info(user_id, first_name, last_name, insta_handle, bio)
        return redirect("/profile/edit")

    # if we are editing profile picture section
    elif form_id == "profile_picture":
        if "file1" not in request.files:
            flash("No Profile Picture found")
            return redirect("/profile")

        f = request.files["file1"]

        result = image_helpers.resize_image_square_crop(f.stream, (100, 100))
        (success, msg, resized_image) = result
        if success == False:
            flash(msg)
            return redirect("/profile/edit")
        else:
            file_name = str(user_id) + ".jpg"
            path = os.path.join(UPLOAD_FOLDER_PROFILE_PICTURE, file_name)
            resized_image.save(path)

            crud.set_user_profile_picture(user_id, file_name)

            # flash("Uploaded picture")
            return redirect("/profile/edit")
    elif form_id == "profile_password":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        #to display an error message we are wrting this conditional
        if crud.update_password_for_user_id(user_id, old_password, new_password) == False:
            flash("Old password is incorrect")
        else:
            flash("Password Updated")
        return redirect("/profile/edit")

    # If it's unknown section
    # we don't know the form_id then display this message
    else:
        flash("Unhandled form submission")
        return redirect("/profile/edit")

    # Update user profile to reflect these new changes.


@app.route("/newlook", methods=["GET"])
def show_newlook_page():
    # Show newlook page
    return render_template("newlook.html")


@app.route("/newlook", methods=["POST"])
def save_newlook_page():
    # Check User Logged In
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]

    index = 0
    file = request.files["file1"]

    # 1 - check input from form. If invalid or missing redirect
    # 2 - Resize the post image and create 1 thumbnail and 1 post image
    # 3 - Create Post in database
    # 4 - Create MakeupImage in database
    # 5 - Save the resized images to folder
    # 6 - Redirect to new post page.

    #import pdb; pdb.set_trace()
    # file1 = image of the post ,
    # check user is sending image file with the request
    if "file1" not in request.files:
        flash("No Post Picture specified")
        return redirect("/newlook")

    post_title = request.form.get("post_title")
    if post_title == None or len(post_title) < 3:
        flash("Post Title is too short")
        return redirect("/newlook")

    post_description = request.form.get("post_description")
    if post_description == None or len(post_description) > 150:
        flash("Post description is too long")
        return redirect("/newlook")

    makeup_type = request.form.get("makeup_type")
    if makeup_type == None or len(makeup_type) > 20:
        flash("Makeup_type is too long")
        return redirect("/newlook")

    (
        thumb_success,
        thumb_msg,
        resized_image_thumb,
    ) = image_helpers.resize_image_square_crop(file.stream, (200, 200))
    (fullres_success, fullres_msg, resized_image_post) = image_helpers.resize_image(
        file.stream, (500, 500)
    )
    if thumb_success == False or fullres_success == False:
        flash(thumb_msg or fullres_msg)
        return redirect("/newlook")
    else:
        # Crud post here
        #
        post = crud.create_post(
            user_id=user_id,
            title=post_title,
            post_description=post_description,
            makeup_type=makeup_type,
        )
        post_id = post.post_id

        # Save post image
        file_name = str.format("{0}_{1}.jpg", post_id, index)
        path = os.path.join(UPLOAD_FOLDER_POST_PICTURES, file_name)
        resized_image_post.save(path)
        # Crud makeup image
        crud.create_makeupimage(post_id=post_id, img_url=file_name)

        # Save thumbnail image
        file_name = str.format("{0}_p.jpg", post_id)
        path = os.path.join(UPLOAD_FOLDER_POST_PICTURES, file_name)
        resized_image_thumb.save(path)

        return redirect(f"/posts/{post_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
