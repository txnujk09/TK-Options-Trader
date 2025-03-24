import pytest
import sys
import os

from app.myapp import create_app 
from app.models import db, Order

def test_place_buy_order():
    app = create_app() #create the app
    app.config.from_object('config.TestConfig') #set the app configuration to test mode

    with app.app_context():
        db.create_all()
        #simulate placing a buy order
        new_order = Order(
            user_id=1, 
            stock_name="AAPL",  # Required field in the model
            option_type="call",  #Specify either "call" or "put"
            order_type="buy", 
            quantity=10, 
            price=100.0
        )
        db.session.add(new_order) #add the order to the database
        db.session.commit()

        #check if order exists in the database
        order = Order.query.filter_by(order_type="buy", user_id=1).first()
        assert order is not None
        assert order.quantity == 10 #q should be 10
        assert order.price == 100.0 #price should be 100.0