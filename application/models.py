from .database import db

class Users(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))