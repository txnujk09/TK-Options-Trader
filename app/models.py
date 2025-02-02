# database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    balance = db.Column(db.Float, default=10000)  # Starting virtual balance

# Options Table
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    strike_price = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    option_type = db.Column(db.String(4), nullable=False)  # 'call' or 'put'
    market_price = db.Column(db.Float, nullable=False)  # Last traded price

# Orders Table
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    order_type = db.Column(db.String(4), nullable=False)  # 'buy' or 'sell'
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), default='pending')  # 'pending' or 'executed'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Trades Table
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Portfolio Table
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
