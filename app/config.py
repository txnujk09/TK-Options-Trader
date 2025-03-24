import os

class Config: #base configuration class
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trading.db' #database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False #disable modification tracking
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super_secret_key" #secret key for the app

class TestConfig(Config): #test configuration class
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' #in-memory database for testing
    TESTING = True #enable testing mode