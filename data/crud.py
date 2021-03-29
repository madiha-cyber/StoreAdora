from model import User, UserProfile, db, Post, Favorites, Product, PostProducts

from datetime import datetime


def create_user(email, password):
    u = User(email=email, password=password)
    db.session.add(u)
    db.session.commit()
    return u


def create_post(user_id, post_description, makeup_type):
    p = Post(
        user_id=user_id, post_description=post_description, makeup_type=makeup_type
    )
    db.session.add(p)
    db.session.commit()
    return p


def create_favorites(user_id, post_id):
    f = Favorites(user_id=user_id, post_id=post_id, date_favorites=datetime.now())
    db.session.add(f)
    db.session.commit()
    return f


def create_product(product_details, website_link, image_url):
    p = Product(
        # product_id=product_id,
        product_details=product_details,
        website_link=website_link,
        image_url=image_url,
    )
    db.session.add(p)
    db.session.commit()
    return p


def create_makeupimage(img_id, post_id, img_url):
    m = MakeupImage(img_id=img_id, post_id=post_id, img_url=img_url)
    db.session.add(m)
    db.session.commit()
    return m


def create_postproducts(product_id, post_id):
    p = PostProducts(product_id=product_id, post_id=post_id)
    db.session.add(p)
    db.session.commit()
    return p
