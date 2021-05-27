from app import db, auth
import config
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    password = db.Column(db.String(192), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        if self not in db.session:
            db.session.add(self)
        db.session.commit()


@auth.verify_password
def verify_password(username, password):
    print(username)
    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return False
    add_user_globel(user)
    return True


def add_user_globel(user):
    config.user = user

