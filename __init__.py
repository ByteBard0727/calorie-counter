from flask import Flask
from flask_cors import CORS
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

    #To setup for hybrid vue flask setup. Cors will be needed for external requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints (routes)
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create the database tables
    with app.app_context():
        db.create_all()

    return app