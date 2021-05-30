from flask import request, jsonify, Blueprint, abort, session
from app.modules.Message import Message
from app.modules.User import User


message_routes = Blueprint("message_routes", __name__, url_prefix="/messages")


@message_routes.route("/read/<int:id>", methods=["GET"])
def read_message(id):
    if not session["username"]:
        abort(400, "please login first!")
    message = Message.query.get(id)
    if not message:
        abort(400, "message not found!\n please try a diffrent id.")
    message.read()

    return jsonify(message.to_json())


@message_routes.route("/delete/<int:id>", methods=["GET"])
def delete_message(id):
    if not session["username"]:
        abort(400, "please login first!")
    message = Message.query.get(id)
    if not message or (
        message.receiverId != session["userID"] and message.sendrId != session["userID"]
    ):
        abort(400, "message not found!\n please try a diffrent id.")

    message.delete()
    return jsonify({"message": f"message {id} was deleted successfuly"})


@message_routes.route("/readall", methods=["GET", "POST"])
def read_all():
    if not session["username"]:
        abort(400, "please login first!")
    if request.method == "GET":
        return jsonify(
            {
                "message": "please post here which users messages you want to see and if you want to see only unread or all"
            }
        )
    try:
        data = request.get_json()
        messages_from = data["username"]
        try:
            onlyunread = data["onlyunread"]
        except:
            onlyunread = False
    except:
        abort(
            400, "you are missing parameters!"
        )  #  message_list = Message.query.filter_by(receiverId=)
    message_list = get_all_messages(
        id=session["userID"], onlyunread=onlyunread, secondId=messages_from
    )
    if not message_list:
        abort(400, "no messeges.")
    for message in message_list:
        if not message.is_read:
            message.is_read = True
            message.save()

    return jsonify([i.to_json() for i in message_list])


@message_routes.route("/readall/sent", methods=["GET", "POST"])
def read_all_sent():
    if not session["username"]:
        abort(400, "please login first!")
    if request.method == "GET":
        return jsonify(
            {
                "message": "please post here which users messages you want to see and if you want to see only unread or all"
            }
        )
    try:
        data = request.get_json()
        messages_to = data["username"]
        try:
            onlyunread = data["onlyunread"]
        except:
            onlyunread = False
    except:
        abort(400, "you are missing parameters!")
    message_list = get_all_messages(
        id=session["userID"], sender=True, onlyunread=onlyunread, secondId=messages_to
    )
    if not message_list:
        abort(400, "no messeges.")

    return jsonify([i.to_json() for i in message_list])


@message_routes.route("/send", methods=["POST"])
def write_message():
    if not session["username"]:
        abort(400, "please login first!")
    try:
        data = request.get_json()
        receiver = data["receiver"]
        subject = data["subject"]
        message = data["message"]

    except:
        abort(400, "you are missing parameters!")
    if User.query.filter_by(username=receiver).first() is None:
        abort(
            400,
            "the user you want to send a message to dosnt exist please try sending somone else!",
        )

    receiverId = User.query.filter_by(username=receiver).first().id
    senderId = session["userID"]
    new_message = Message(senderId, receiverId, subject, message)
    new_message.save()
    return jsonify({"messege": f"your message was swnt to {receiver}"})


## get list of all messages by id of sender or receiver
def get_all_messages(id, sender=False, onlyunread=False, secondId="all"):
    """
    the function gets 4 parameters:
    id: the id of the user rquesting the messages
    sender: a bool parameter the is true if id belonges to sender of the message
    onlyunread: bool parameter that is true if requested onlyunread messages
    seconedId: id of the user you want to read your messages with or all for all messages

    the function returns a list of messages according to what was requested
    """

    # if the request is from sender
    if sender:
        # if requested for specific user message
        if not secondId == "all":
            # if requested for only unread messages
            if onlyunread:
                return Message.query.filter_by(
                    sendrId=id, receiverId=secondId, is_read=False
                ).all()
        # if requsted messages from all users
        # if requested for only unread message
        if onlyunread:
            return Message.query.filter_by(sendrId=id, is_read=False).all()
        # if requested all users and all messages
        return Message.query.filter_by(sendrId=id).all()

    # if not requested by sender
    # if requested for specific user message
    if not secondId == "all":
        # if requested for only unread messages
        if onlyunread:
            return Message.query.filter_by(
                sendrId=secondId, receiverId=id, is_read=False
            ).all()
    # if requsted messages from all users
    # if requested for only unread messages
    if onlyunread:
        return Message.query.filter_by(receiverId=id, is_read=False).all()
    # if requested all users and all messages
    return Message.query.filter_by(receiverId=id).all()

