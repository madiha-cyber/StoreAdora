"""Server for StoreAdora flask_app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
import os
import crud
import image_helpers

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import validators
from app import flask_app

UPLOAD_FOLDER_PROFILE_PICTURE = "./static/images/profile/"
UPLOAD_FOLDER_POST_PICTURES = "./static/images/posts/"
UPLOAD_FOLDER_PRODUCT_PICTURES = "./static/images/products/"

###############################################################################
# Helper Functions
###############################################################################
def is_user_signed_in():
    """
    Check if user's session exists
    """
    # return "user_id" in session and session["user_id"] is not None
    return session.get("user_id") is not None


def flash_errors(form):
    """
    Flashes form errors
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                f"Error: '{getattr(form, field).label.text}' - {error}",
                "error",
            )


###############################################################################
# Login Related Forms & Functions
###############################################################################
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[validators.DataRequired(), validators.Email()],
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(), validators.Length(min=6, max=35)],
    )


@flask_app.route("/login", methods=["GET"])
def show_login_page():
    """
    Show Login page
    """

    # Check User Logged In Already
    if is_user_signed_in():
        return redirect("/profile")

    form = LoginForm()

    # If session does not exists display login page
    return render_template("login.html", form=form)


@flask_app.route("/login", methods=["POST"])
def login_user():
    """
    Login the user and redirect to /profile page
    """

    # Check User Logged In Already
    if is_user_signed_in():
        return redirect("/profile")

    form = LoginForm()
    if not form.validate_on_submit():
        flash_errors(form)
        return redirect("/login")

    user = crud.get_user_by_email_and_password(form.email.data, form.password.data)
    if not user:
        flash("Invalid email/password")
        return redirect("/login")
    else:
        session["user_id"] = user.user_id
        return redirect("/profile")


@flask_app.route("/logout", methods=["GET"])
def logout_user():
    """
    logout the user
    """
    # Check User Logged In Already
    if is_user_signed_in():
        del session["user_id"]
    return redirect("/")


###############################################################################
# Signup Related Forms & Functions
###############################################################################
class SignupForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[validators.DataRequired(), validators.Email()],
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(), validators.Length(min=6, max=35)],
    )
    first_name = StringField(
        "First Name",
        validators=[validators.DataRequired(), validators.Length(min=3, max=35)],
    )
    last_name = StringField(
        "Last Name",
        validators=[validators.DataRequired(), validators.Length(min=3, max=35)],
    )


@flask_app.route("/signup", methods=["GET"])
def show_signup_page():
    """
    Show Signup page
    """
    # Check User Logged In Already
    if is_user_signed_in():
        return redirect("/")

    form = SignupForm()
    return render_template("signup.html", form=form)


@flask_app.route("/signup", methods=["POST"])
def signup_user():
    """
    Create new Account then redirect to /profile page
    """
    # Check User Logged In Already
    if is_user_signed_in():
        return redirect("/")

    form = SignupForm()
    if not form.validate_on_submit():
        flash_errors(form)
        return redirect("/signup")

    # Make sure we don't allow same email again.
    existing_user = crud.get_user_by_email(form.email.data)

    if existing_user:
        flash("This email is already in use.")
        return redirect("/signup")
    else:
        # create a new user and store its value in the session
        user = crud.create_user_and_profile(
            form.first_name.data,
            form.last_name.data,
            form.email.data,
            form.password.data,
        )
        session["user_id"] = user.user_id
        return redirect("/profile")


###############################################################################
# Home Page Functions
###############################################################################
@flask_app.route("/")
def homepage():
    """
    View homepage
    """
    posts = crud.get_posts(max_posts=12)
    return render_template("homepage.html", posts=posts)


###############################################################################
# New Look Related Forms & Functions
###############################################################################
class NewLookForm(FlaskForm):
    description = StringField(
        "Description",
        validators=[validators.DataRequired(), validators.Length(min=10, max=200)],
    )
    title = StringField(
        "Title",
        validators=[validators.DataRequired(), validators.Length(min=6, max=35)],
    )
    images = FileField(validators=[FileRequired()])
    makeup_type = StringField("Makeup Type", validators=[validators.DataRequired()])
    products = StringField("Products")


@flask_app.route("/newlook", methods=["GET"])
def show_newlook_page():
    """
    Show newlook page
    """
    form = NewLookForm()
    return render_template("newlook.html", form=form)


@flask_app.route("/newlook", methods=["POST"])
def save_newlook_page():
    """
    Create new look
    """

    # Check User Logged In Already
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]

    form = NewLookForm()
    if not form.validate_on_submit():
        flash_errors(form)
        return redirect("/newlook")

    # 1 - check input from form. If invalid or missing redirect
    # 2 - Resize the post image and create 1 thumbnail and 1 post image
    # 3 - Create Post in database
    # 4 - Create MakeupImage in database
    # 5 - Save the resized images to folder
    # 6 - Redirect to new post page.

    # check user is sending image file with the request

    index = 0
    results = []

    # Create thumbnail image
    (
        thumb_success,
        thumb_msg,
        resized_image_thumb,
    ) = image_helpers.resize_image_square_crop(
        request.files.getlist("images")[0].stream, (200, 200)
    )

    if thumb_success is False:
        flash(thumb_msg)
        return redirect("/newlook")

    # Create resized post images
    for file in request.files.getlist("images"):
        r = image_helpers.resize_image(file.stream)
        results.append(r)

        (fullres_success, fullres_msg, resized_image_post) = r
        if fullres_success is False:
            flash(thumb_msg or fullres_msg)
            return redirect("/newlook")

    # Store all resized post images and thumbnails here
    post = crud.create_post(
        user_id=user_id,
        title=form.title.data,
        post_description=form.description.data,
        makeup_type=form.makeup_type.data,
        products=request.form.getlist("products"),
    )
    post_id = post.post_id

    file_name = f"{post_id}_p.jpg"
    path = os.path.join(UPLOAD_FOLDER_POST_PICTURES, file_name)
    resized_image_thumb.save(path)

    for result in results:
        (fullres_success, fullres_msg, resized_image_post) = result

        # Save post image
        file_name = str.format("{0}_{1}.jpg", post_id, index)
        path = os.path.join(UPLOAD_FOLDER_POST_PICTURES, file_name)
        resized_image_post.save(path)

        # Add to the database
        crud.create_makeupimage(post_id=post_id, image=file_name)
        index += 1
    return redirect(f"/posts/{post_id}")


###############################################################################
# Posts related Functions
###############################################################################
@flask_app.route("/posts")
def get_all_posts():
    """
    View all posts
    """

    posts = crud.get_posts()
    return render_template("all_posts.html", posts=posts)


@flask_app.route("/posts/<post_id>")
def get_post(post_id):
    """
    View each post
    """

    post = crud.get_post(post_id)
    products = crud.get_products_for_post(post_id)
    post_images = crud.get_post_images(post_id)
    comments = crud.get_comments_by_post_id(post_id)

    return render_template(
        "post_details.html",
        post=post,
        products=products,
        post_images=post_images,
        comments=comments,
    )


###############################################################################
# User related Functions
###############################################################################
@flask_app.route("/user/<user_id>")
def show_user(user_id):
    """
    Show details on a particular user.
    """
    user = crud.get_user_by_id(user_id)
    if not user:
        return render_template("user_profile_not_found.html")

    userprofile = crud.get_user_profile(user_id)
    posts = crud.get_posts_for_user(user_id=user_id)
    return render_template(
        "user_profile.html", user=user, userprofile=userprofile, posts=posts
    )


@flask_app.route("/user/<user_id>/favorites")
def show_user_favorites(user_id):
    """
    Show Favorites of a particular user.
    """
    user = crud.get_user_by_id(user_id)
    if not user:
        return render_template("user_profile_not_found.html")

    return render_template("favorites.html", posts=crud.get_user_favorites(user_id))


###############################################################################
# Profile related Functions
###############################################################################
@flask_app.route("/profile", methods=["GET"])
def show_userprofile():
    """
    Home page for logged in user.
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]

    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)
    user_posts = crud.get_posts_for_user(user_id)

    return render_template(
        "profile.html", user=user, userprofile=userprofile, posts=user_posts
    )


@flask_app.route("/profile/edit", methods=["GET"])
def show_edit_profile_page():
    """
    Show edit profile page.
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    userprofile = crud.get_user_profile(user_id)
    return render_template("edit_profile.html", user=user, userprofile=userprofile)


@flask_app.route("/profile/edit", methods=["POST"])
def save_edit_profile():
    """
    Save edit profile changes
    """
    # Check User Logged In Already
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

        result = image_helpers.resize_image_square_crop(f.stream, (400, 400))
        (success, msg, resized_image) = result
        if success is False:
            flash(msg)
            return redirect("/profile/edit")
        else:
            file_name = f"{user_id}.jpg"
            path = os.path.join(UPLOAD_FOLDER_PROFILE_PICTURE, file_name)
            resized_image.save(path)

            crud.set_user_profile_picture(user_id, file_name)

            # flash("Uploaded picture")
            return redirect("/profile/edit")
    elif form_id == "profile_password":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        # to display an error message we are wrting this conditional
        if (
            crud.update_password_for_user_id(user_id, old_password, new_password)
            is False
        ):
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


###############################################################################
# Post related Functions
###############################################################################
@flask_app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post_by_user(post_id):
    if not is_user_signed_in():
        return redirect("/")

    post = crud.get_post(post_id)
    if not post:
        return redirect("/")

    user_id = session["user_id"]

    crud.delete_post_by_user(user_id=user_id, post_id=post_id)

    return redirect("/profile")


@flask_app.route("/posts/<post_id>/edit", methods=["GET"])
def show_edit_post_page(post_id):
    """
    Edit Post Page
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return redirect("/")

    post = crud.get_post(post_id)
    if not post:
        return redirect("/")

    products = crud.get_products_for_post(post_id)
    post_images = crud.get_post_images(post_id)

    if post.user_id != session["user_id"]:
        return redirect("/")

    return render_template(
        "edit_post.html", post=post, post_images=post_images, products=products
    )


@flask_app.route("/posts/<post_id>/edit", methods=["POST"])
def save_edit_post_page(post_id):
    """
    Edit Post Page
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return redirect("/")

    form_id = request.form.get("form_id")

    if form_id == "basic_info":
        title = request.form.get("title")
        post_description = request.form.get("post_description")
        makeup_type = request.form.get("makeup_type")

        crud.update_post_info(post_id, title, post_description, makeup_type)

        # return redirect("posts/<post_id>/edit")
    elif form_id == "post_image":

        if "images" not in request.files:
            flash("No image found")
            return redirect(f"/posts/{post_id}/edit")

        index = len(crud.get_post(post_id=post_id).makeupimages)
        results = []

        # Create thumbnail image
        (
            thumb_success,
            thumb_msg,
            resized_image_thumb,
        ) = image_helpers.resize_image_square_crop(
            request.files.getlist("images")[0].stream, (200, 200)
        )

        if thumb_success is False:
            flash(thumb_msg)
            return redirect(f"/posts/{post_id}/edit")

        # Create resized post images
        for file in request.files.getlist("images"):
            r = image_helpers.resize_image(file.stream)
            results.append(r)

            (fullres_success, fullres_msg, resized_image_post) = r
            if fullres_success is False:
                flash(thumb_msg or fullres_msg)
                return redirect(f"/posts/{post_id}/edit")

        # Store all resized post images and thumbnails here
        # Save thumbnail image
        file_name = str.format("{0}_p.jpg", post_id)
        path = os.path.join(UPLOAD_FOLDER_POST_PICTURES, file_name)
        resized_image_thumb.save(path)

        for result in results:
            (fullres_success, fullres_msg, resized_image_post) = result

            # Save post image
            file_name = str.format("{0}_{1}.jpg", post_id, index)
            path = os.path.join(UPLOAD_FOLDER_POST_PICTURES, file_name)
            resized_image_post.save(path)

            # Add to the database
            crud.create_makeupimage(post_id=post_id, image=file_name)
            index += 1

        return redirect(f"/posts/{post_id}")

    return render_template(f"/posts/{post_id}")


###############################################################################
# New Product related Functions
###############################################################################
class NewProductForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[validators.DataRequired(), validators.Length(min=6, max=35)],
    )
    details = StringField(
        "Details",
        validators=[validators.DataRequired(), validators.Length(min=6, max=35)],
    )
    url = StringField(
        "Url",
        validators=[validators.DataRequired(), validators.Length(min=6)],
    )
    picture = FileField("Picture", validators=[FileRequired()])


@flask_app.route("/newproduct", methods=["GET"])
def display_product_page():
    """
    Display a new product
    """
    return render_template("newproduct.html", form=NewProductForm())


@flask_app.route("/newproduct", methods=["POST"])
def add_a_new_product():
    """
    Adds a new product
    """

    if not is_user_signed_in():
        return redirect("/newproduct")

    form = NewProductForm()
    if not form.validate_on_submit():
        flash_errors(form)
        return redirect("/newproduct")

    f = request.files["picture"]

    result = image_helpers.resize_image_square_crop(f.stream, (50, 50))
    (success, msg, resized_image) = result
    if success is False:
        flash(msg)
        return redirect("/newproduct")
    else:
        p = crud.create_product(
            details=form.details.data, title=form.title.data, url=form.url.data
        )
        file_name = f"{p.product_id}.jpg"
        path = os.path.join(UPLOAD_FOLDER_PRODUCT_PICTURES, file_name)
        resized_image.save(path)
        crud.set_product_image(product_id=p.product_id, image=file_name)

        return redirect("/profile")


@flask_app.route("/products/add", methods=["POST"])
def add_product():
    """
    Add new Product to DB
    """
    if not is_user_signed_in():
        return redirect("/")

    title = request.form.get("title")
    details = request.form.get("details")
    url = request.form.get("url")
    product = crud.create_product(details=details, title=title, url=url)
    return jsonify(product)


###############################################################################
# Search related Functions
###############################################################################
@flask_app.route("/products/search.json", methods=["GET"])
def search_product_by_name():
    """
    Search Product that match the name in DB
    """
    name = request.args.get("q")
    if name is None:
        return jsonify({})

    results = crud.get_products_by_name(name)

    return jsonify(results)


###############################################################################
# Favorites related Functions
###############################################################################
@flask_app.route("/favorites/user/<post_id>", methods=["GET"])
def get_is_post_favorite_by_user(post_id):
    """
    Is this post in user's favorite?
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return jsonify({})
    user_id = session["user_id"]
    result = crud.get_is_post_favorite_by_user(user_id=user_id, post_id=post_id)
    if result is not None:
        return jsonify({"id": result.favorites_id})
    else:
        return jsonify({})


@flask_app.route("/favorites/user/add/<post_id>", methods=["GET"])
def add_post_to_user_favorites(post_id):
    """
    Add a post to user's favorites
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return jsonify({})

    user_id = session["user_id"]
    p = crud.get_post(post_id=post_id)
    if p is None:
        return jsonify({})

    u = crud.get_is_post_favorite_by_user(user_id=user_id, post_id=post_id)
    if u is not None:
        return jsonify({"id": u.favorites_id})

    f = crud.create_favorites(user_id=user_id, post_id=post_id)
    return jsonify({"id": f.favorites_id})


@flask_app.route("/favorites/user/remove/<post_id>", methods=["GET"])
def remove_post_from_user_favorites(post_id):
    """
    Remove a post from user's favorites
    """
    # Check User Logged In Already
    if not is_user_signed_in():
        return jsonify({})

    user_id = session["user_id"]
    p = crud.get_post(post_id=post_id)
    if p is None:
        return jsonify({})

    fav = crud.get_is_post_favorite_by_user(user_id=user_id, post_id=post_id)
    if fav is None:
        return jsonify({})

    id = fav.favorites_id
    r = crud.remove_post_from_user_favorites(user_id=user_id, post_id=post_id)
    if r is not None:
        return jsonify({"id": id})
    return jsonify({})


###############################################################################
# Comment related Functions
###############################################################################
@flask_app.route("/posts/<post_id>/comment", methods=["POST"])
def add_comment_from_post_page(post_id):

    if not is_user_signed_in():
        return redirect("/")

    post = crud.get_post(post_id)
    if not post:
        return redirect("/")

    user_id = session["user_id"]
    comment = request.form.get("comment")

    crud.create_comment(user_id=user_id, post_id=post_id, text=comment)
    return redirect(f"/posts/{post_id}")


@flask_app.route("/posts/<post_id>/comments/<comment_id>/delete", methods=["POST"])
def delete_comment_from_post(post_id, comment_id):

    if not is_user_signed_in():
        return redirect("/")

    user_id = session["user_id"]

    crud.delete_comment(user_id=user_id, comment_id=comment_id)
    flash("Comment deleted")
    return redirect(f"/posts/{post_id}")


###############################################################################
# Search Functions
###############################################################################
@flask_app.route("/search", methods=["GET"])
def search():
    search_text = request.args.get("search_text")

    posts = crud.search_posts(search_text=search_text)
    return render_template("search.html", search_text=search_text, posts=posts)


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=True)
