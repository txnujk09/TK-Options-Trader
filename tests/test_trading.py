import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/monte_carlo')))

print(sys.path)

from app.myapp import create_app
from app.models import db, Order

def test_place_buy_order():
    app = create_app()
    app.config.from_object('config.TestConfig')

    with app.app_context():
        db.create_all()
        #simulate placing a buy order
        new_order = Order(user_id=1, option_id=1, order_type="buy", quantity=10, price=100.0)
        db.session.add(new_order)
        db.session.commit()

        # Check if order exists in the database
        order = Order.query.filter_by(order_type="buy", user_id=1).first()
        assert order is not None
        assert order.quantity == 10
        assert order.price == 100.0