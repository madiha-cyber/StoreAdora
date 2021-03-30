"""Server for StoreAdora app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from data.model import connect_to_db

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
#app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

# @app.route('/posts')
# def all_posts():
#     "View all posts"
#  posts = crud.get_posts()

#  return render_template('all_posts.html', posts=posts)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
