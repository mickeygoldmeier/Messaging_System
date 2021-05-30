from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Data model for user accounts.
        the class containes in id, username, hased password and the date the user was created."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    password = db.Column(db.String(192), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # class method for hashing the password
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    # class method for verifeing password when user wants to signin
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # save to db after changes were made or add to db if its anew user
    def save(self):
        if self not in db.session:
            db.session.add(self)
        db.session.commit()

