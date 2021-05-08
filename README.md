# StoreAdora

## Overview

StoreAdora, a visual platform,  enables users to learn and share different makeup looks. Users can browse through many looks created by the influencers. Along with that, they can see what products were used in those looks and where to buy them.

This web application is a fully functional web application which allows user to register, login/logout, create new posts, add new products, manage favorites, edit profile, search and much more.

When you open the web application you are presented with top looks created by the influencers. You can then continue browsing through the website as an anonymous user, or you can sign-up/login to get an enhanced experience. When you are logged in you get much more options such as the ability to create a new look, add looks to your favorites, add new products, and comment on posts.


## Demo

[![Final Project](https://img.youtube.com/vi/WZE2Jo0jE3c/0.jpg)](https://www.youtube.com/watch?v=WZE2Jo0jE3c "Final Project")


## Technologies required (besides typical Hackbright tech stack)
- Python
  - Jinja
  - Flask
  - FlaskForms
  - Pillow
  - SQLAlchemy
  - Faker
- PostgreSQL
- HTML
- Javascript
- AJAX
- Bootstrap


## Screenshots
![Homepage Screenshot](readme/1.jpg "Homepage")
![Post Screenshot](readme/2.jpg "Post")
![Post Screenshot](readme/3.jpg "Post")
![Search Screenshot](readme/4.jpg "Search")

## DataModel
- User email, password, name
- User's insta_handle & bio
- Product tile, description and website link
- Makeup title, description and makeup type
- Favorites


![DataModel Screenshot](readme/datamodel.png "DataModel")

## Roadmap

#### 3.0 (current)
- Complete Sample Data
- Bootstrap + CSS Styling
- Full text search
- Comments add/delete.
- Form validation with FlaskForm

#### 2.0
- Update the UI
- User can comment on post.
- Use AJAX to set/get Favorite for better experience.
- Use AJAX to search and select products for new look.

#### MVP (1.0)
- Users can view categories of makeup looks.
- Users can login/ logout.
- Users can create their own account.
- Users can create posts.
- Uers can upload photos and add product descrption.
- Users can click on the website link of each product.
- User can have favorite posts.
- Users can Edit their profile, add profile picture edit their personal information.

# How to

## Setup & Run

IMPORTANT!! This requires that you already have PostgreSQL installed. If you have not done that already please do that by following this link: https://wiki.postgresql.org/wiki/PostgreSQL_For_Development_With_Vagrant

Here are step by step instructions:

* In your terminal type: `git clone https://github.com/madihagoheer/StoreAdora.git`
* Go to the folder: `cd StoreAdora`
* Setup virtualenv via:
  * On mac/linux run: `virtualenv env`
  * On windows run: `virtualenv env --always-copy`
* Enter virtualenv via: `source env/bin/activate`
* Install required python libraries via: `pip3 install -r requirements.txt`
* Setup the data and seed with sample data with: `python3 seed_data.py`
* Launch the web app using: `python3 server.py`
* To view this web app in browser simply follow this link: **http://localhost:5000**


Once the website is up and running you can either create new account, or use these accounts that were added as part of seed_data.
|email|password|
|--|--|
|email1@outlook.com|password|
|email2@outlook.com|password|
|email3@outlook.com|password|


## Running tests

CAUTION!!! This section assumes that you have already completed the "Setup & Run" section above.
### Run Tests Only
You can run tests with
```
python3 tests.py
```
### Run Tests and Detailed Code Coverage Report
Run these
```
coverage run --source=. tests.py
coverage html
```
Once you run these commands the report will be stored in a new folder called "htmlcov". You can view that report by opening **[htmlconv/index.html](htmlconv/index.html)** in browser.

### Run Tests and Small Code Coverage Report

```
coverage run --source=. tests.py
coverage report -m
```