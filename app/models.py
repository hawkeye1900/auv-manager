from . import db, bcrypt
from flask_login import UserMixin


# auv model/table
class AUV(db.Model):
    __tablename__ = 'auv'

    # define table columns/fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<AUV id={self.id} name='{self.name}'>"

    # convert table row into a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }

# User model to handle authentication and password checking
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
