from data.model import (
    User,
    UserProfile,
    db,
    Post,
    Favorite,
    Product,
    PostProducts,
    MakeupImage,
    Comment,
)

from sqlalchemy import or_

from datetime import datetime


def create_user(email, password):
    """
    """
    u = User(email=email, password=password)
    db.session.add(u)
    db.session.commit()
    return u


def create_post(user_id, title, post_description, makeup_type, products=[]):
    """
    """
    p = Post(
        user_id=user_id,
        title=title,
        post_description=post_description,
        makeup_type=makeup_type,
    )
    db.session.add(p)
    db.session.commit()
    if products:
        for product in products:
            p.products.append(Product.query.get(product))
        db.session.commit()
    return p


def create_favorites(user_id, post_id):
    """
    """

    f = Favorite.query.filter(Favorite.user_id == user_id).filter(Favorite.post_id==post_id).all()
    if f:
        return f[0]

    f = Favorite(user_id=user_id, post_id=post_id, date_favorites=datetime.now())
    db.session.add(f)
    db.session.commit()
    return f


def load_favorites(user_id):
    """
    """
    return Favorite.query.filter(Favorite.user_id == user_id).all()


def get_is_post_favorite_by_user(user_id, post_id):
    """
    checks if post is favorite by the user
    """

    return (
        Favorite.query.filter(Favorite.user_id == user_id)
        .filter(Favorite.post_id == post_id)
        .first()
    )


def remove_post_from_user_favorites(user_id, post_id):
    """
    """

    result = (
        Favorite.query.filter(Favorite.user_id == user_id)
        .filter(Favorite.post_id == post_id)
        .delete()
    )
    db.session.commit()
    return result


def create_product(title, details, url=None, image=None):
    """
    """
    p = Product(
        title=title,
        details=details,
        url=url,
        image=image,
    )
    db.session.add(p)
    db.session.commit()
    return p


# Adding image in the product after creating a new product in the databse we got a new product_id
def set_product_image(product_id, image):
    """
    """

    p = Product.query.get(product_id)
    p.image = image
    db.session.commit()


def create_makeupimage(post_id, image):
    """
    """
    m = MakeupImage(post_id=post_id, image=image)
    db.session.add(m)
    db.session.commit()
    return m


def create_postproducts(product_id, post_id):
    """
    """
    p = PostProducts(product_id=product_id, post_id=post_id)
    db.session.add(p)
    db.session.commit()
    return p


def create_user_and_profile(f_name, l_name, email, password):
    """
    Create new user with email & password.
    Then create userprofile with first_name & last_name.
    """
    u = create_user(email=email, password=password)
    p = UserProfile(first_name=f_name, last_name=l_name, user_id=u.user_id)
    db.session.add(p)
    db.session.commit()
    return u


def get_posts(max_posts=None):
    """
    Return all posts
    """
    if not max_posts:
        return Post.query.all()
    else:
        return Post.query.limit(max_posts).all()


def search_posts(search_text, max_posts=15):
    """
    Return all posts
    """
    if not search_text:
        return []

    return (
        Post.query.filter(
            or_(
                Post.post_description.ilike(f"%{search_text}%"),
                Post.title.ilike(f"%{search_text}%"),
                Post.makeup_type.ilike(f"%{search_text}%"),
            )
        )
        .limit(max_posts)
        .all()
    )


def get_products_for_post(post_id):
    """
    Return all the products in a post
    """

    return (
        Product.query.join(PostProducts).filter(PostProducts.post_id == post_id).all()
    )


def get_post(post_id):
    """
    """
    return Post.query.filter(Post.post_id == post_id).first()


def get_user_by_email_and_password(email, password):
    """
    Return a user by email and password
    """
    # user = User.query.filter(User.email == email).first()
    # if user.password == password:
    #   return user
    # else:
    #   (something about wrong password)

    # shorter version
    # return user if user.password == password else 'Wrong password'

    # return User.query.filter(User.email == email).filter(User.password == password).first()
    return (
        User.query.filter(User.email == email).filter(User.password == password).first()
    )


def get_user_profile(user_id):
    """
    Return user profile for each user
    """

    return UserProfile.query.filter(UserProfile.user_id == user_id).first()


def get_user_favorites(user_id):
    """
    """
    return User.query.get(user_id).favorites


# >>> madiha = User.query.get(1)
# <User user_id=1 email='madiha@gmail.com' ... >
# >>> madiha.user_profile.insta_handle
# 'madiha_insta_handle'
# >>> madiha.posts
# [<Post id=1...>, <Post id=2...>, ...]
# >>> for post in madiha.posts:
# ...     <a href=post.id>post.name</a>


def get_user_by_id(user_id):
    """
    """
    return User.query.filter(User.user_id == user_id).first()


def get_user_by_email(email):
    """
    Return user by email
    """
    return User.query.filter(User.email == email).first()


def set_user_profile_picture(user_id, file_name):
    p = UserProfile.query.get(user_id)
    p.profile_picture = file_name
    db.session.commit()


def get_post_images(post_id):
    """
    """
    return MakeupImage.query.filter(MakeupImage.post_id == post_id).all()


def get_posts_for_user(user_id):
    """
    """
    return Post.query.filter(Post.user_id == user_id).all()


def update_user_profile_info(user_id, first_name, last_name, insta_handle, bio):
    """
    updates userprofile
    """
    db.session.query(UserProfile.user_id == user_id).update(
        {
            "first_name": first_name,
            "last_name": last_name,
            "insta_handle": insta_handle,
            "bio": bio,
        }
    )
    db.session.commit()


def update_post_info(post_id, title, post_description, makeup_type):
    """
    updates users post
    """
    db.session.query(Post.post_id == post_id).update(
        {
            "title": title,
            "post_description": post_description,
            "makeup_type": makeup_type,
            # details :details
        }
    )
    db.session.commit()


def update_password_for_user_id(user_id, old_password, new_password):
    """
    updates password
    """

    user = (
        User.query.filter(User.user_id == user_id)
        .filter(User.password == old_password)
        .first()
    )
    if not user:
        return False

    db.session.query(User.user_id == user_id).update(
        {
            "password": new_password,
        }
    )

    db.session.commit()
    return True


def get_products_by_name(name):
    """
    return products by their name
    """
    return Product.query.filter(
        or_(
            Product.title.ilike(f"%{name}%"),
            Product.details.ilike(f"%{name}%")
        )
    ).all()


def get_comments_by_post_id(post_id):
    """
    return comments made by a user on a post
    """

    return Comment.query.filter(Comment.post_id == post_id).all()


def create_comment(user_id, post_id, text):
    """
    create a comment by a user
    """

    c = Comment(user_id=user_id, post_id=post_id, text=text)
    db.session.add(c)
    db.session.commit()


def delete_comment(user_id, comment_id):
    """
    deletes comment by user
    """

    c = (
        Comment.query.filter(Comment.user_id == user_id)
        .filter(Comment.comment_id == comment_id)
        .first()
    )

    # check if there is a comment_id created by this user_id
    if c == None:
        return

    db.session.delete(c)
    db.session.commit()


def delete_post_by_user(user_id, post_id):
    """
    deletes post by the user who created that post
    """
    # checking if the owner/user of the post is this user"
    c = (
        Post.query.filter(Post.user_id == user_id)
        .filter(Post.post_id == post_id)
        .first()
    )

    if c == None:
        return
    db.session.delete(c)
    db.session.commit()
