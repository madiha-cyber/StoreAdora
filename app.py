from flask import Flask

from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__, static_url_path="/static")
flask_app.secret_key = "dev"
flask_app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# flask_app.jinja_env.undefined = StrictUndefined
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///finalproject"
flask_app.config["SQLALCHEMY_ECHO"] = False
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(flask_app)


def connect_to_db(flask_app, db_uri):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
