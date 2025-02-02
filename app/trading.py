from models import db, Order, Trade, User

def match_orders():
    buy_orders = Order.query.filter_by(order_type="buy", status="pending").order_by(Order.price.desc()).all()
    sell_orders = Order.query.filter_by(order_type="sell", status="pending").order_by(Order.price.asc()).all()

    executed_trades = []

    while buy_orders and sell_orders:
        buy_order = buy_orders[0]
        sell_order = sell_orders[0]

        if buy_order.price >= sell_order.price:
            trade_price = sell_order.price
            trade_quantity = min(buy_order.quantity, sell_order.quantity)

            # Update buyer and seller balances
            buyer = User.query.get(buy_order.user_id)
            seller = User.query.get(sell_order.user_id)

            buyer.balance -= trade_price * trade_quantity
            seller.balance += trade_price * trade_quantity

            # Update order quantities
            buy_order.quantity -= trade_quantity
            sell_order.quantity -= trade_quantity

            # Record trade
            new_trade = Trade(
                buyer_id=buy_order.user_id,
                seller_id=sell_order.user_id,
                option_id=buy_order.option_id,
                price=trade_price,
                quantity=trade_quantity
            )
            db.session.add(new_trade)
            executed_trades.append(new_trade)

            # Remove fully executed orders
            if buy_order.quantity == 0:
                db.session.delete(buy_order)
            if sell_order.quantity == 0:
                db.session.delete(sell_order)

            db.session.commit()

    return executed_trades