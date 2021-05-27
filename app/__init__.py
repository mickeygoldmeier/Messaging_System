# Import flask and template operators

from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# Define the WSGI application object
app = Flask(__name__)
CORS(app)
# Configurations
app.config.from_pyfile("../config.py")

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

from app.routes.user_routes import user_routes
from app.routes.message_routes import message_routes

app.register_blueprint(user_routes)
app.register_blueprint(message_routes)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

