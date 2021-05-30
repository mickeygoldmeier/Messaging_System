from flask import request, jsonify, Blueprint, abort, session
from datetime import datetime as dt
from app import db, app
import json
from app.modules.User import User


user_routes = Blueprint("user_routs", __name__)


@user_routes.route("/register", methods=["POST"])
def register():

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
    return (jsonify({"username": user.username}), 201)


@user_routes.route("/login", methods=["POST"])
def login():
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

    if not session["username"]:
        abort(401, "you are not logged in yet!")
    session["username"] = None
    return jsonify({"message": "you are logged out now"})
