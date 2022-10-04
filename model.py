from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    password = db.Column(db.String(250))
    handler = db.Column(db.String(250))

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handler = db.Column(db.String(250), db.ForeignKey('users.handler'))
    content = db.Column(db.String(280))
