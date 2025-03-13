# database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #imports the 'UserMixin' class from Flask-Login

db = SQLAlchemy()

# User Table
class User(UserMixin, db.Model): #defines a user model with authentication support and database integration
    id = db.Column(db.Integer, primary_key=True) #unique user ID (primary key)
    username = db.Column(db.String(80), unique=True, nullable=False) #unique username
    hashed_password = db.Column(db.String(256), nullable=False) #hashed pwd for security
    email = db.Column(db.String(256), nullable=False) #user email
    balance = db.Column(db.Float, default=10000)  # Starting virtual balance

    #method to set a user's password (encrypts before storing)
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    #method to check if the given pwd matches the stored hashed pwd
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    #method to update user's email
    def set_email(self, email):
        self.email = email

# Options Table
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique option ID (primary key)
    stock_symbol = db.Column(db.String(10), nullable=False) #ticker symbol of stock 
    strike_price = db.Column(db.Float, nullable=False) #strike price at which option can be exercised
    expiration_date = db.Column(db.DateTime, nullable=False) #expiration date of option
    option_type = db.Column(db.String(4), nullable=False)  # type of option: 'call' or 'put'
    market_price = db.Column(db.Float, nullable=False)  # Last traded price

# Orders Table
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique order ID (primary key)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key linking to 'User' table
    stock_name = db.Column(db.String, nullable=False) #stock ticker symbol
    option_type = db.Column(db.String(4), nullable=False) # Option type: 'call' or 'put'
    order_type = db.Column(db.String(4), nullable=False)  # Order type: 'buy' or 'sell'
    quantity = db.Column(db.Integer, nullable=False) #no. of contracts in order
    price = db.Column(db.Float, nullable=False) #price at which order is placed
    status = db.Column(db.String(10), default='pending')  #order status: 'pending' or 'executed'
    timestamp = db.Column(db.DateTime, default=datetime.now()) #timestamp of when order was placed

# Trades Table
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique trade ID (primary key)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key linking to buyer ('User')
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key linking to seller ('User')
    stock_name = db.Column(db.String, nullable=False) #ticker symbol of stock
    option_type = db.Column(db.String(4), nullable=False) #type of option: 'call' or 'put'
    price = db.Column(db.Float, nullable=False) #price at which trade was executed
    quantity = db.Column(db.Integer, nullable=False) #number of contracts traded
    timestamp = db.Column(db.DateTime, default=datetime.now()) #time when trade was executed

# Portfolio Table
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique portfolio entry ID (primary key)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key linking to 'User' table
    stock_name = db.Column(db.String, nullable=False) #ticker symbol of stock
    quantity = db.Column(db.Integer, nullable=False) #number of contracts owned
    value=db.Column(db.Float, nullable=False) #total market value of holdings
