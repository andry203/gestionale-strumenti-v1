from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.routes import dashboard
from config import config

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
    from app.models import Utente

    @login_manager.user_loader
    def load_user(user_id):
        return Utente.query.get(int(user_id))

    # Configure Flask-Login

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Blueprint registrations
    
    from app.routes import auth, strumenti, richieste, dashboard

    app.register_blueprint(auth.bp)
    app.register_blueprint(strumenti.bp)
    app.register_blueprint(richieste.bp)
    app.register_blueprint(dashboard.bp)

    return app
