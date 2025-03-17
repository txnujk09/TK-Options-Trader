from flask import Flask, current_app #import necessary Flask components
from flask_migrate import Migrate #imports for handling database migrations
from models import db #import database instance from models
from routes import routes #import routes blueprint for registering routes

migrate = Migrate() #initialise flask-migrate

def create_app():
    #application factory function to create and configure a flask app instance
    app = Flask(__name__, static_folder='static') #create the Flask app instance and specify the directory for static files
    app.config.from_object('config.Config')  # Load app configurations

    #initialise extensions
    db.init_app(app) #associate database with app
    migrate.init_app(app, db) #attach flask-migrate to handle migrations

    #creating database tables
    with app.app_context(): #ensure database tables are created inside an app context
        print("Current app:", current_app.name) #print current app name for debugging
        db.create_all() #create all tables

    # Register Blueprints
    app.register_blueprint(routes)

    return app #return configured flask app instance

