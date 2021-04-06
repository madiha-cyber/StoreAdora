import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from data.model import UserProfile, db, connect_to_db
from crud import *
from datetime import datetime


def create(
    email,
    password,
    first_name,
    last_name,
    insta_handle,
    bio,
    post_title,
    post_description,
    makeup_type,
    post_image,
):
    u = create_user(email=email, password=password)
    p = UserProfile(
        user_id=u.user_id,
        first_name=first_name,
        last_name=last_name,
        insta_handle=insta_handle,
        bio=bio,
    )
    o = create_post(
        user_id=u.user_id,
        title=post_title,
        post_description=post_description,
        makeup_type=makeup_type,
    )
    i = create_makeupimage(o.post_id, post_image)
    return u


def add_sample_data():

    users_list = []
    profiles_list = []
    posts_list = []
    favorites_list = []
    products_list = []

    u = create(
        email="madihagoheer@outlook.com",
        password="123",
        first_name="madiha",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        post_title="Dramatic makeup",
        post_description="This is a look that I created using tis",
        makeup_type="Dramatic",
        post_image="1_1.jpg",
    )
    users_list.append(u)

    u = create(
        email="madiha_latif@outlook.com",
        password="123",
        first_name="madiha",
        last_name="Latif",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        post_title="Dramatic makeup",
        post_description="This is a look that I created using tis",
        makeup_type="Dramatic",
        post_image="2_1.jpg",
    )
    users_list.append(u)

    u = create(
        email="asimgoheer@outlook.com",
        password="123",
        first_name="Asim",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        post_title="Dramatic makeup",
        post_description="This is a look that I created using tis",
        makeup_type="Dramatic",
        post_image="3_1.jpg",
    )
    users_list.append(u)

    u = create(
        email="myreengoheer@outlook.com",
        password="123",
        first_name="Myreen",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        post_title="Dramatic makeup",
        post_description="This is a look that I created using tis",
        makeup_type="Dramatic",
        post_image="4_1.jpg",
    )
    users_list.append(u)

    # # User 1
    # u = create_user(email="madihagoheer@outlook.com", password="123")
    # p = UserProfile(
    #     user_id=u.user_id,
    #     first_name="Madiha",
    #     last_name="Goheer",
    #     insta_handle="@madihagoheerofficial",
    #     bio="Makeup Artist",
    # )
    # users_list.append(u)
    # profiles_list.append(p)

    # # User 2
    # u = create_user(email="asimgoheer@outlook.com", password="123")
    # p = UserProfile(
    #     user_id=u.user_id,
    #     first_name="Myreen",
    #     last_name="Goheer",
    #     insta_handle="@asimgoheerofficial",
    #     bio="Makeup Blogger",
    # )
    # users_list.append(u)
    # profiles_list.append(p)

    # # User 3
    # u = create_user(email="myreen@hotmail.com", password="123")
    # p = UserProfile(user_id=u.user_id, insta_handle="@myreengoheerofficial")
    # users_list.append(u)
    # profiles_list.append(p)

    # Product 1
    p = create_product(
        "Foundation",
        "Nars Longwear",
        "https://www.sephora.com/",
        "/static/images/foundation1.jpg",
    )
    products_list.append(p)

    # Product 2
    p = create_product(
        "Concealer",
        "Huda Beauty",
        "https://www.sephora.com/",
        "/static/images/foundation1.jpg",
    )
    products_list.append(p)

    # # User 1 Post 1
    # p = create_post(
    #     user_id=users_list[0].user_id,
    #     title="Dramatic Makeup",
    #     post_description="This is a dummy post",
    #     makeup_type="Dramatic",
    # )
    # posts_list.append(p)
    # create_postproducts(products_list[0].product_id, p.post_id)

    # # user 1 Post 2
    # p = create_post(
    #     user_id=users_list[0].user_id,
    #     title="Classic Makeup",
    #     post_description="This is a dummy post 2",
    #     makeup_type="Classic",
    # )
    # posts_list.append(p)
    # create_postproducts(products_list[0].product_id, p.post_id)
    # create_postproducts(products_list[1].product_id, p.post_id)

    # # User 2 Favorites 1
    # f = create_favorites(user_id=users_list[1].user_id, post_id=posts_list[0].post_id)
    # favorites_list.append(f)

    # # User 2 Favorites 2
    # f = create_favorites(user_id=users_list[1].user_id, post_id=posts_list[1].post_id)
    # favorites_list.append(f)

    db.session.add_all(profiles_list)
    db.session.commit()

    print("Added objects to DB")


if __name__ == "__main__":
    from flask import Flask

    os.system("dropdb finalproject")
    os.system("createdb finalproject")

    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
    add_sample_data()
