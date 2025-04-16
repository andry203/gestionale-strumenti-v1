from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from app.routes import auth, strumenti, richieste, utenti

# Initialization extensions

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    
    # Main instance of Flask app

    app = Flask(__name__)

    # Configuration from config.py

    app.config.from_object(config)

    # Connect extensions to Flask app

    db.init_app(app)
    login_manager.init_app(app)

    from app import models

    # Configure Flask-Login

    login_manager.login_view = 'auth.login'                     # nome della route di login                         REMOVE COMMENT
    login_manager.login_message_category = 'info'               # stile messaggio (usato nei flash messages)        REMOVE COMMENT

    # Blueprint registrations
    
    app.register_blueprint(auth.bp)
    # app.register_blueprint(strumenti.bp)
    # app.register_blueprint(richieste.bp)
    # app.register_blueprint(utenti.bp)

    return app
