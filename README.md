# StoreAdora
## Project Proposal

### Overview

A visual platform for users where they can post creative makeup looks and also check various makeup looks posted by other influencers.

### Technologies required (besides typical Hackbright tech stack)
- Python
- Jinga
- PostgresSQL
- HTML
- Javascript
- Ajax
- Bootstrap

### Data
- User email, password, name
- User's insta_handle & bio
- Product tile, description and website link
- Makeup title, description and makeup type
- Favorites

## Screenshots
![Homepage Screenshot](readme/1.jpg "Homepage")
![Post Screenshot](readme/2.jpg "Post")
![Post Screenshot](readme/3.jpg "Post")
![Search Screenshot](readme/4.jpg "Search")

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

# How to Run
## Setup
```
pip3 install -r requirements.txt
```
## Initialize Sample Data
```
python3 sampledata.py
```
## Run
```
python3 server.py
```
