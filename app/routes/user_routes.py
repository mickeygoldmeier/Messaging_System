from flask import request, jsonify, Blueprint, abort
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
    user_data = request.get_json()
    new_user = User(user_data["username"], user_data["password"])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "regresration successful"})
