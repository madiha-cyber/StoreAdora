import os
import json
from random import choice, randint, sample
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

        p.products.extend(post["products"])
        u.posts.append(p)
        db.session.commit()

    return u


def add_sample_data():

    looks_list = ["Dramatic", "Wedding", "Classic", "Runway", "Special Effects"]

    products_list = [
        create_product(
            "Face Brushes",
            "PRO Concealer Brush #57",
            "https://www.sephora.com/product/pro-airbrush-concealer-brush-57-P313020",
            "1.webp",
        ),
        create_product(
            "Face Brushes",
            "FENTY BEAUTY by Rihanna : Portable Contour & Concealer Brush 150",
            "https://www.sephora.com/product/portable-contour-concealer-brush-150-P34587546",
            "2.webp",
        ),
        create_product(
            "Concealer",
            "Huda Beauty Nude Obsessions Eyeshadow Palette",
            "https://www.sephora.com/product/nude-obsessions-eyeshadow-palette-P450887",
            "3.webp",
        ),
        create_product(
            "Tinted Moisturizer Oil",
            "Laura Mercier: Tinted Moisturizer Oil Free Natural Skin Perfector Broad Spectrum SPF 20",
            "https://www.sephora.com/product/tinted-moisturizer-broad-spectrum-oil-free-P140906?icid2=new%20arrivals:p140906:product",
            "4.webp",
        ),
        create_product(
            "Tinted Moisturizer",
            "NARS: Pure Radiant Tinted Moisturizer Broad Spectrum SPF 30",
            "https://www.sephora.com/product/pure-radiant-tinted-moisturizer-spf-30-pa-P302923",
            "5.webp",
        ),
        create_product(
            "Eye Pallettes",
            "HUDA BEAUTY : The New Nude Eyeshadow Palette",
            "https://www.sephora.com/product/the-new-nude-eyeshadow-palette-P43818047?skuId=2137289&icid2=products%20grid:p43818047:product",
            "6.webp",
        ),
        create_product(
            "Foundation",
            "NARS: Sheer Glow Foundation",
            "https://www.sephora.com/product/sheer-glow-foundation-P247355",
            "7.webp",
        ),
        create_product(
            "Concealer",
            "NARS: Radiant Creamy Concealer",
            "https://www.sephora.com/product/radiant-creamy-concealer-P377873",
            "8.webp",
        ),
        create_product(
            "Concealer",
            "Kosas: Revealer Super Creamy + Brightening Concealer and Daytime Eye Cream",
            "https://www.sephora.com/product/kosas-revealer-concealer-P456151",
            "9.webp",
        ),
        create_product(
            "Concealer",
            "Yves Saint Laurent: Touche Eclat High Cover Radiant Under-Eye Concealer",
            "https://www.sephora.com/product/touche-eclat-high-cover-radiant-concealer-P440971",
            "10.webp",
        ),
        create_product(
            "Eye Pallets",
            "HUDA BEAUTY : Pastel Obsessions Eyeshadow Palette",
            "https://www.sephora.com/product/huda-beauty-pastel-obsessions-eyeshadow-palette-P489310288",
            "11.webp",
        ),
    ]

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
                "makeup_type": choice(looks_list),
                "images": ["1_0.jpg", "1_1.jpg", "1_2.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "LA PERLE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["2_0.jpg", "2_1.jpg", "2_2.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "AMATO",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["3_0.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "SPLASH",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["4_0.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "MARIE CLAIRE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["5_0.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "SPACE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["6_0.jpg", "6_1.jpg", "6_2.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "SPLASH 2012",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["7_0.jpg", "7_1.jpg", "7_2.jpg"],
                "products": sample(products_list, 5),
            },
        ],
        profile_picture="1.jpg",
    )

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
                "makeup_type": choice(looks_list),
                "images": ["8_0.jpg", "8_1.jpg", "8_2.jpg", "8_3.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "HOUSE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["9_0.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "STEPHEN",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["10_0.jpg", "10_1.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "GQ MAGAZINE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["11_0.jpg", "11_1.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "ELLE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["12_0.jpg", "12_1.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "SUMMER",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["13_0.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "WINTER",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["14_0.jpg"],
                "products": sample(products_list, 5),
            },
        ],
        profile_picture="2.jpg",
    )

    u = create(
        email="madihagoheer@outlook.com",
        password="123456",
        first_name="Madiha",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        posts=[
            {
                "title": "SPRING",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["15_0.jpg", "15_1.jpg", "15_2.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "AUTUM",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["16_0.jpg", "16_1.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "BEACH",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["17_0.jpg", "17_1.jpg"],
                "products": sample(products_list, 5),
            },
        ],
        profile_picture="3.jpg",
    )

    u = create(
        email="myreengoheer@outlook.com",
        password="123456",
        first_name="Myreen",
        last_name="Goheer",
        insta_handle="@madihagoheerofficial",
        bio="Some test bio",
        posts=[
            {
                "title": "SNOW",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["18_0.jpg", "18_1.jpg", "18_2.jpg"],
                "products": sample(products_list, 5),
            },
            {
                "title": "ICE",
                "description": faker.paragraph(),
                "makeup_type": choice(looks_list),
                "images": ["19_0.jpg", "19_1.jpg", "19_2.jpg"],
                "products": sample(products_list, 5),
            },
        ],
        profile_picture="1.jpg",
    )

    # Create random comments
    for post_id in range(1, 19):
        for comment_count in range(randint(1, 10)):
            create_comment(randint(1, 4), post_id, faker.paragraph())

    # Create Favorites
    for user_id in range(1, 4):
        for _ in range(1, randint(5, 10)):
            create_favorites(user_id, randint(1, 19))

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
