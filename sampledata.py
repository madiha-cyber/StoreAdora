import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from data.model import UserProfile, db, connect_to_db
from crud import *
from datetime import datetime
from faker import Faker


def create(
    email,
    password,
    first_name,
    last_name,
    insta_handle,
    bio,
    posts,
    profile_picture,
    products=[],
):
    u = create_user(email=email, password=password)
    u.userprofiles.append(
        UserProfile(
            user_id=u.user_id,
            first_name=first_name,
            last_name=last_name,
            insta_handle=insta_handle,
            bio=bio,
            profile_picture=profile_picture,
        )
    )
    for post in posts:
        p = Post(
            user_id=u.user_id,
            title=post["title"],
            post_description=post["description"],
            makeup_type=post["makeup_type"],
        )
        for post_image in post["images"]:
            p.makeupimages.append(MakeupImage(image=post_image))

        p.products.append(
            Product(
                title="Foundation",
                details="Nars Longwear",
                url="https://www.sephora.com/",
                image="1.png",
            )
        )
        u.posts.append(p)
        db.session.commit()

    # for product in products:
    #     create_postproducts(product.product_id, o.post_id)
    return u


def add_sample_data():

    users_list = []
    profiles_list = []
    posts_list = []
    favorites_list = []
    products_list = []

    # Product 1
    p = create_product(
        "Foundation",
        "Nars Longwear",
        "https://www.sephora.com/",
        "1.png",
    )
    products_list.append(p)

    # Product 2
    p = create_product(
        "Concealer",
        "Huda Beauty Concealer for Dark Skin",
        "https://www.sephora.com/",
        "2.png",
    )
    products_list.append(p)

    # Product 3
    p = create_product(
        "Concealer",
        "Huda Beauty Concealer For Light Skin",
        "https://www.sephora.com/",
        "3.png",
    )
    products_list.append(p)

    # Product 4
    p = create_product(
        "Concealer",
        "Huda Beauty makeup brushes",
        "https://www.sephora.com/",
        "1.png",
    )
    products_list.append(p)

    faker = Faker()

    u = create(
        email="amanda@outlook.com",
        password="123456",
        first_name="Amanda",
        last_name="Cerney",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        posts=[
            {
                "title": "NATIVE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["1_0.jpg", "1_1.jpg", "1_2.jpg"],
            },
            {
                "title": "LA PERLE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["2_0.jpg", "2_1.jpg", "2_2.jpg"],
            },
            {
                "title": "AMATO",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["3_0.jpg"],
            },
            {
                "title": "SPLASH",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["4_0.jpg"],
            },
            {
                "title": "MARIE CLAIRE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["5_0.jpg"],
            },
            {
                "title": "SPACE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["6_0.jpg", "6_1.jpg", "6_2.jpg"],
            },
            {
                "title": "SPLASH 2012",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["7_0.jpg", "7_1.jpg", "7_2.jpg"],
            },
        ],
        profile_picture="1.jpg",
        products=products_list,
    )
    users_list.append(u)

    u = create(
        email="huda@outlook.com",
        password="123456",
        first_name="madiha",
        last_name="Latif",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        posts=[
            {
                "title": "GROVE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["8_0.jpg", "8_1.jpg", "8_2.jpg", "8_3.jpg"],
            },
            {
                "title": "HOUSE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["9_0.jpg", "9_1.jpg"],
            },
            {
                "title": "STEPHEN",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["10_0.jpg", "10_1.jpg"],
            },
            {
                "title": "GQ MAGAZINE",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["11_0.jpg", "11_1.jpg"],
            },
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["12_0.jpg", "12_1.jpg"],
            },
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["13_0.jpg"],
            },
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["14_0.jpg"],
            },
        ],
        profile_picture="2.jpg",
        products=products_list,
    )
    users_list.append(u)

    u = create(
        email="madihagoheer@outlook.com",
        password="123456",
        first_name="Madiha",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        posts=[
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["15_0.jpg", "15_1.jpg", "15_2.jpg"],
            },
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["16_0.jpg", "16_1.jpg"],
            },
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["17_0.jpg", "17_1.jpg"],
            },
        ],
        profile_picture="3.jpg",
        products=products_list,
    )
    users_list.append(u)

    u = create(
        email="myreengoheer@outlook.com",
        password="123456",
        first_name="Myreen",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        posts=[
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["18_0.jpg", "18_1.jpg", "18_2.jpg"],
            },
            {
                "title": "Dramatic Makeup",
                "description": faker.paragraph(),
                "makeup_type": "Dramatic",
                "images": ["19_0.jpg", "19_1.jpg", "19_2.jpg"],
            },
        ],
        profile_picture="1.jpg",
        products=products_list,
    )
    users_list.append(u)

    for post_id in range(1, 19):
        for comment_count in range(randint(1, 10)):
            create_comment(randint(1, 4), post_id, faker.paragraph())

    db.session.add_all(profiles_list)
    db.session.commit()

    print("Added objects to DB")


def add_sample_images():
    os.system("cp -r data/sampledata/* static/images/")


if __name__ == "__main__":
    from flask import Flask

    os.system("rm -r static/images/profile/*.jpg")
    os.system("rm -r static/images/products/*")
    os.system("rm -r static/images/posts/*.jpg")
    os.system("dropdb finalproject")
    os.system("createdb finalproject")

    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
    add_sample_data()
    add_sample_images()
