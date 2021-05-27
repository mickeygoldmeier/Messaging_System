from flask import request, jsonify, Blueprint, abort
from datetime import datetime as dt
from app import db, app, auth
import json
import config
from app.modules.Message import Message


message_routes = Blueprint("message_routes", __name__)


@message_routes.route("/message/read/<int:id>", methods=["GET"])
def get_message(id):
    message = Message.query.get(id)
    if not message:
        abort(400, "message not found!\n please try a diffrent id.")
    message.read()

    return jsonify(message.to_json())


@message_routes.route("/messages/readall/<unread>", methods=["GET"])
def get_all_message(unread):
    if not unread:
        pass  #  message_list = Message.query.filter_by(receiverId=)
    message = Message.query.filter(id)
    if not message:
        abort(400, "message not found!\n please try a diffrent id.")
    message.is_read = True
    message.save()

    return jsonify(message.to_json())


@message_routes.route("/message/write", methods=["POST"])
@auth.login_required
def write_message():
    message = request.get_json()

    return jsonify({"hi": config.user})

    if not message:
        abort(400)

    return jsonify(message)

