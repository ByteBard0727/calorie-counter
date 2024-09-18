from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig
from datetime import datetime, timedelta

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints (routes)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create the database tables
    with app.app_context():
        db.create_all()

    return app