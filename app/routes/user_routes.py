from flask import request, jsonify, Blueprint, abort, session
from app.modules.User import User


user_routes = Blueprint("user_routs", __name__)


@user_routes.route("/register", methods=["POST"])
def register():
    """
    the register function is also a route the user can register to our system from.
    it gets post requests with json data about username and password
    the function checks that their isnt any other user with the same name.
    and registers the user
    """
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
    except:
        abort(400, "you are missing parameters!")

        # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400, "user already exists!")  # existing user
    user = User(username=username)
    user.hash_password(password)
    user.save()
    return (
        jsonify(
            {
                "message": f"hello {user.username} you are now part of our messaging system"
            }
        ),
        201,
    )


@user_routes.route("/login", methods=["POST"])
def login():
    """
    the login function gets post requests with username and password in body
    makes sure the user exists and the password is correct and then saves the user name and id to session
    for further use and to keep him loged in
    """
    if not session["username"]:
        abort(401, "you are already logged in please logout first!")
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
    except:
        abort(400, "you are missing parameters!")

    user = User.query.filter_by(username=username).first()
    if not user.verify_password(password):
        abort(401, "password or user name are worng please try again or register!")
    session["username"] = username
    session["userID"] = user.id
    return jsonify({"message": "you are logged in now"})


@user_routes.route("/logout", methods=["POST", "GET"])
def logout():
    """
    the logout function gets both types of requests get and post 
    and logs the user out of the system by deleting him from the session
    """
    if not session["username"]:
        abort(401, "you are not logged in yet!")
    session["username"] = None
    return jsonify({"message": "you are logged out now"})
