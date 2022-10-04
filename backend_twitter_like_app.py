from flask import Flask
from model import db, ma

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app=app)
    ma.init_app(app=app)
    with app.app_context():
        db.create_all()
    return app