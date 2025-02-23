from models import db, Order, Trade, User, Portfolio
from datetime import datetime

# def match_orders():
#     buy_orders = Order.query.filter_by(order_type="buy", status="pending").order_by(Order.price.desc()).all()
#     sell_orders = Order.query.filter_by(order_type="sell", status="pending").order_by(Order.price.asc()).all()

#     executed_trades = []

#     while buy_orders and sell_orders:
#         buy_order = buy_orders[0]
#         sell_order = sell_orders[0]

#         if buy_order.price >= sell_order.price:
#             trade_price = sell_order.price
#             trade_quantity = min(buy_order.quantity, sell_order.quantity)

#             # Update buyer and seller balances
#             buyer = User.query.get(buy_order.user_id)
#             seller = User.query.get(sell_order.user_id)

#             buyer.balance -= trade_price * trade_quantity
#             seller.balance += trade_price * trade_quantity

#             # Update order quantities
#             buy_order.quantity -= trade_quantity
#             sell_order.quantity -= trade_quantity

#             # Record trade
#             new_trade = Trade(
#                 buyer_id=buy_order.user_id,
#                 seller_id=sell_order.user_id,
#                 option_id=buy_order.option_id,
#                 price=trade_price,
#                 quantity=trade_quantity
#             )
#             db.session.add(new_trade)
#             executed_trades.append(new_trade)

#             # Remove fully executed orders
#             if buy_order.quantity == 0:
#                 db.session.delete(buy_order)
#             if sell_order.quantity == 0:
#                 db.session.delete(sell_order)

#             db.session.commit()

#     return executed_trades

def update_portfolio(stock:str, quantity:float, value:float, user_id:int, trade_type:str):
    # Get stock for the user
    #user_portfolios = Portfolio.query.filter(Portfolio.user_id==user_id).all()
    user_stock_details = db.session.query(Portfolio).filter_by(user_id=user_id, stock_name=stock).first()
    print("update_portfolio", user_stock_details)
    
    if user_stock_details:
        print("Upadting existing stock")
        # If trade type is SELL reduce the quantity and holdings value
        if trade_type == 'SELL':
            user_stock_details.quantity = user_stock_details.quantity - quantity
            user_stock_details.value = user_stock_details.value - value
            
        else: # Buy increase quantity and value
            user_stock_details.quantity = user_stock_details.quantity + quantity
            user_stock_details.value = user_stock_details.value + value

        updated_stock_value = user_stock_details.value
        db.session.commit()  
    else:
        print("Adding new stock")
        portfolio = Portfolio()
        portfolio.user_id = user_id
        portfolio.stock_name = stock
        portfolio.quantity =  -quantity if trade_type == 'SELL' else quantity
        portfolio.value = -value if trade_type == 'SELL' else value
        updated_stock_value = portfolio.value
        db.session.add(portfolio)
        db.session.commit()

    update_user_available_balance(updated_stock_value, user_id, trade_type)
            

def update_user_available_balance(value:float, user_id:int, trade_type:str):
    # Get user
    user = db.session.query(User).filter_by(id=user_id).first()
    print("User old balance=", user.balance)
    # If user is found
    if user:
        # If trade type SELL increase the balance
        if trade_type == 'SELL':
            new_balance = user.balance + value
        # If trade type SELL increase the balance
        else:
            new_balance = user.balance - value

        user.balance = new_balance

    print("User new balance=", user.balance)
    db.session.commit()  

def merge_sort_orders(orders, ascending=True):
    """Sorts a list of orders using Merge Sort."""
    if len(orders) <= 1:
        return orders

    mid = len(orders) // 2
    left_half = merge_sort_orders(orders[:mid], ascending)
    right_half = merge_sort_orders(orders[mid:], ascending)

    return merge(left_half, right_half, ascending)

def merge(left, right, ascending):
    """Merges two sorted halves into a single sorted list."""
    sorted_orders = []
    i = j = 0

    while i < len(left) and j < len(right):
        if (ascending and left[i].price < right[j].price) or (not ascending and left[i].price > right[j].price):
            sorted_orders.append(left[i])
            i += 1
        else:
            sorted_orders.append(right[j])
            j += 1

    sorted_orders.extend(left[i:])
    sorted_orders.extend(right[j:])
    
    return sorted_orders

def match_orders():
    """Matches buy and sell orders using Merge Sort for sorting."""
    
    # Fetch all pending orders WITHOUT sorting in SQL
    buy_orders = list(Order.query.filter_by(order_type="BUY", status="pending"))
    sell_orders = list(Order.query.filter_by(order_type="SELL", status="pending"))

    # Sort orders using Merge Sort
    buy_orders = merge_sort_orders(buy_orders, ascending=False)  # Sort buy orders by price DESC
    sell_orders = merge_sort_orders(sell_orders, ascending=True)  # Sort sell orders by price ASC

    executed_trades = []
  
    for buy_order in buy_orders:
        print("In Buy order")
        # Check all the put orders
        for sell_order in sell_orders:
            print("In Sell order")
            if buy_order.stock_name == sell_order.stock_name:
                if buy_order.price >= sell_order.price:
                    trade_price = sell_order.price
                    trade_quantity = min(buy_order.quantity, sell_order.quantity)
                    buy_order.quantity -= trade_quantity
                    sell_order.quantity -= trade_quantity

                    # Update buyer and seller balances
                    buy_order_user = User.query.get(buy_order.user_id)
                    sell_orders_user = User.query.get(sell_order.user_id)

                    buy_order_user.balance -= trade_price * trade_quantity
                    sell_orders_user.balance += trade_price * trade_quantity
                    print("Adding trade record")
                    # Record trade
                    new_trade = Trade(
                        buyer_id=buy_order.user_id,
                        seller_id=sell_order.user_id,
                        stock_name=buy_order.stock_name,
                        price=trade_price,
                        quantity=trade_quantity,
                        option_type=buy_order.option_type,
                        timestamp = datetime.now()
                    )
                    db.session.add(new_trade)
                    db.session.commit()

                    # Now update buyers and sellers portfolio
                    trade_value = trade_quantity * trade_price
                    update_portfolio(buy_order.stock_name, trade_quantity, trade_value, buy_order.user_id, 'BUY')
                    update_portfolio(sell_order.stock_name, trade_quantity, trade_value, sell_order.user_id, 'SELL')


                    # Remove fully executed orders
                    if buy_order.quantity == 0:
                        db.session.delete(buy_order)
                    if sell_order.quantity == 0:
                        db.session.delete(sell_order)

                    db.session.commit()           


