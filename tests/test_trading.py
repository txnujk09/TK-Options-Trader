from app.myapp import create_app, db
from app.models import Order, db

def test_place_buy_order():
    app = create_app()
    app.config.from_object('config.TestConfig')

    with app.app_context():
        # Simulate placing a buy order
        new_order = Order(user_id=1, option_id=1, order_type="buy", quantity=10, price=100.0)
        db.session.add(new_order)
        db.session.commit()

        # Check if order exists in the database
        order = Order.query.filter_by(order_type="buy", user_id=1).first()
        assert order is not None
        assert order.quantity == 10
        assert order.price == 100.0