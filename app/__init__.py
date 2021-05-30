# Import flask ,SQLAlchemy and session
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


# Define the WSGI application object
app = Flask(__name__)
# Define the database object
db = SQLAlchemy(app)
# Define the session object
sess = Session()
# set Configurations
app.config.from_pyfile("../config.py")
# initiolize session with flask app
sess.init_app(app)

# import routes so we can register them to our app
from app.routes.user_routes import user_routes
from app.routes.message_routes import message_routes

# register routes to app
app.register_blueprint(user_routes)
app.register_blueprint(message_routes)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

