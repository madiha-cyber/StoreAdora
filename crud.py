from data.model import (
    User,
    UserProfile,
    db,
    Post,
    Favorites,
    Product,
    PostProducts,
    MakeupImage,
)

from datetime import datetime


def create_user(email, password):
    """"""
    u = User(email=email, password=password)
    db.session.add(u)
    db.session.commit()
    return u


def create_post(user_id, title, post_description, makeup_type):
    """"""
    p = Post(
        user_id=user_id,
        title=title,
        post_description=post_description,
        makeup_type=makeup_type,
    )
    db.session.add(p)
    db.session.commit()
    return p


def create_favorites(user_id, post_id):
    """"""
    f = Favorites(user_id=user_id, post_id=post_id, date_favorites=datetime.now())
    db.session.add(f)
    db.session.commit()
    return f


def create_product(product_details, title, website_link=None, image_url=None):
    """"""
    p = Product(
        title=title,
        product_details=product_details,
        website_link=website_link,
        image_url=image_url,
    )
    db.session.add(p)
    db.session.commit()
    return p


def create_makeupimage(post_id, img_url):
    """"""
    m = MakeupImage(post_id=post_id, img_url=img_url)
    db.session.add(m)
    db.session.commit()
    return m


def create_postproducts(product_id, post_id):
    """"""
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


def get_posts():
    """
    Return all posts
    """

    return Post.query.all()


def get_products_for_post(post_id):
    """
    Return all the products in a post
    """

    return (
        Product.query.join(PostProducts).filter(PostProducts.post_id == post_id).all()
    )


def get_post(post_id):
    """"""
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


# >>> madiha = User.query.get(1)
# <User user_id=1 email='madiha@gmail.com' ... >
# >>> madiha.user_profile.insta_handle
# 'madiha_insta_handle'
# >>> madiha.posts
# [<Post id=1...>, <Post id=2...>, ...]
# >>> for post in madiha.posts:
# ...     <a href=post.id>post.name</a>


def get_user_by_id(user_id):
    """"""
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
    """"""
    return MakeupImage.query.filter(MakeupImage.post_id == post_id).all()


def get_posts_for_user(user_id):
    """"""
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
    return Product.query.filter(Product.title.ilike(str.format("%{}%", name))).all()
