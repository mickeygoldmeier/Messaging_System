# Define the application directory
import os
from os import environ

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = bool(environ.get("SQLALCHEMY_TRACK_MODIFICATIONS"))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = int(environ.get("THREADS_PER_PAGE"))

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = bool(environ.get("CSRF_ENABLED"))

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = environ.get("CSRF_SESSION_KEY")

# Secret key for signing cookies
SECRET_KEY = environ.get("SECRET_KEY")

# session
SESSION_PERMANENT = bool(environ.get("SESSION_PERMANENT"))
SESSION_TYPE = environ.get("SESSION_TYPE")
