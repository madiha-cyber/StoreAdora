"""Server for StoreAdora app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from data.model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
#app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/posts')
def get_all_posts():
    """View all posts"""

    posts = crud.get_posts()

    return render_template('all_posts.html', all_posts=posts)

@app.route('/posts/<post_id>')
def get_post(post_id):
    if post_id != None:
        return crud.get_post(int(post_id))
    else:
        return "No ID"


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
