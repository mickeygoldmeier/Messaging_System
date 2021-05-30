from app import db


class Message(db.Model):
    """
    Data model for messages.

    the class containes an id, a forgin key to sender and receiver, 
    the subject and the nessage, is_read and the date the nessage was created.

    """

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sendrId = db.Column(db.Integer, db.ForeignKey("users.id"))
    receiverId = db.Column(db.Integer, db.ForeignKey("users.id"))
    sender = db.relationship("User", foreign_keys=sendrId)
    receiver = db.relationship("User", foreign_keys=receiverId)
    message = db.Column(db.Text, index=False, unique=False, nullable=False)
    subject = db.Column(db.String(80), index=False, unique=False, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # constructor for the class
    def __init__(self, senderId, receiverId, message, subject):
        self.sendrId = senderId
        self.receiverId = receiverId
        self.message = message
        self.subject = subject

    # save to db after changes were made or add to db if its a new message
    def save(self):
        if self not in db.session:
            db.session.add(self)
        db.session.commit()

    # delete message
    def delete(self):
        db.session.add(self)
        db.session.commit()

    # read the message / changes is_read to false and saves to db
    def read(self):
        self.is_read = True
        self.save()

    # returns a json format of all the parameters we will want to show the user
    def to_json(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "subject": self.subject,
            "message": self.message,
            "sent on": self.date_created,
        }
