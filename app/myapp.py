from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from routes import routes

#db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load app configurations

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    #creating database tables
    with app.app_context():
        print("Current app:", current_app.name)
        db.create_all()

    # Register Blueprints
    app.register_blueprint(routes)

    return app

