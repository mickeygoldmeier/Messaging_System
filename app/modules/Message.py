from app import db


class Message(db.Model):
    """Data model for user accounts."""

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

    def __init__(self, senderId, receiverId, message, subject):
        self.sendrId = senderId
        self.receiverId = receiverId
        self.message = message
        self.subject = subject

    def save(self):
        if self not in db.session:
            db.session.add(self)
        db.session.commit()

    def read(self):
        self.is_read = True
        self.save()

    def to_json(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "subject": self.subject,
            "message": self.message,
            "sent on": self.date_created,
        }
