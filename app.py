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
