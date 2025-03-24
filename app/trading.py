from models import db, Order, Trade, User, Portfolio
from datetime import datetime

def update_portfolio(stock:str, quantity:float, value:float, user_id:int, trade_type:str): #update the user's portfolio with the new trade
    user_stock_details = db.session.query(Portfolio).filter_by(user_id=user_id, stock_name=stock).first() #get the user's stock details
    print("update_portfolio", user_stock_details)
    
    if user_stock_details:
        print("Upadting existing stock")
        #if trade type is SELL reduce the quantity and holdings value
        if trade_type == 'SELL':
            user_stock_details.quantity = user_stock_details.quantity - quantity #reduce the quantity
            user_stock_details.value = user_stock_details.value - value #reduce the value
            
        else: # Buy increase quantity and value
            user_stock_details.quantity = user_stock_details.quantity + quantity #increase the quantity
            user_stock_details.value = user_stock_details.value + value #increase the value

        updated_stock_value = user_stock_details.value
        db.session.commit()   #commit the transaction
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

    update_user_available_balance(updated_stock_value, user_id, trade_type) #update the user's available balance
            

def update_user_available_balance(value:float, user_id:int, trade_type:str):
    # Get user
    user = db.session.query(User).filter_by(id=user_id).first()
    print("User old balance=", user.balance)
    # If user is found
    if user:
        # If trade type SELL increase the balance
        if trade_type == 'SELL':
            new_balance = user.balance + value #increase the balance
        else:
            new_balance = user.balance - value #reduce the balance

        user.balance = new_balance

    print("User new balance=", user.balance)
    db.session.commit()  

def merge_sort_orders(orders, ascending=True): #sorts in ascending order if true
    """Sorts a list of orders using Merge Sort."""
    if len(orders) <= 1: # Base case: list is already sorted
        return orders

    mid = len(orders) // 2 #find middle index to split the list into two halves
    left_half = merge_sort_orders(orders[:mid], ascending) #sort the left half recursively
    right_half = merge_sort_orders(orders[mid:], ascending) #sort the right half recursively

    return merge(left_half, right_half, ascending) #merge the two sorted halves and return the result

def merge(left, right, ascending): 
    """Merges two sorted halves into a single sorted list."""
    sorted_orders = [] #initialise an empty list to store the sorted orders
    i = j = 0  #initialise pointers for the left and right halves

    while i < len(left) and j < len(right): #iterate through the left and right halves
        if (ascending and left[i].price < right[j].price) or (not ascending and left[i].price > right[j].price): #compare the prices of the orders
            sorted_orders.append(left[i]) #append the smaller order to the sorted list
            i += 1 #increment the pointer for the left half
        else:
            sorted_orders.append(right[j]) #append the smaller order to the sorted list
            j += 1 #increment the pointer for the right half

    sorted_orders.extend(left[i:]) #append any remaining orders from the left half
    sorted_orders.extend(right[j:]) #append any remaining orders from the right half
    
    return sorted_orders #return the sorted list

def match_orders(): 
    """Matches buy and sell orders using Merge Sort for sorting."""
    
    buy_orders = list(Order.query.filter_by(order_type="BUY", status="pending")) #get all pending buy orders
    sell_orders = list(Order.query.filter_by(order_type="SELL", status="pending")) #get all pending sell orders

    # Sort orders using Merge Sort
    buy_orders = merge_sort_orders(buy_orders, ascending=False)  #sort buy orders by price DESC
    sell_orders = merge_sort_orders(sell_orders, ascending=True)  #sort sell orders by price ASC

    executed_trades = [] #initialise an empty list to store executed trades
  
    for buy_order in buy_orders: #iterate through the buy orders
        print("In Buy order") 
        # Check all the put orders
        for sell_order in sell_orders: #iterate through the sell orders
            print("In Sell order")
            if buy_order.stock_name == sell_order.stock_name: #check if the orders are for the same stock
                if buy_order.price >= sell_order.price: #check if the buy price is greater than or equal to the sell price
                    trade_price = sell_order.price #set the trade price to the sell price
                    trade_quantity = min(buy_order.quantity, sell_order.quantity) #set the trade quantity to the minimum of the buy and sell quantities
                    buy_order.quantity -= trade_quantity #reduce the buy order quantity by the trade quantity
                    sell_order.quantity -= trade_quantity #reduce the sell order quantity by the trade quantity

                    # Update buyer and seller balances
                    buy_order_user = User.query.get(buy_order.user_id) #get the buyer user
                    sell_orders_user = User.query.get(sell_order.user_id) #get the seller user

                    buy_order_user.balance -= trade_price * trade_quantity #reduce the buyer balance by the trade value
                    sell_orders_user.balance += trade_price * trade_quantity #increase the seller balance by the trade value
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
                    db.session.add(new_trade) #add the trade to the database
                    db.session.commit() #commit the transaction

                    # Now update buyers and sellers portfolio
                    trade_value = trade_quantity * trade_price
                    update_portfolio(buy_order.stock_name, trade_quantity, trade_value, buy_order.user_id, 'BUY') 
                    update_portfolio(sell_order.stock_name, trade_quantity, trade_value, sell_order.user_id, 'SELL')


                    # Remove fully executed orders
                    if buy_order.quantity == 0: #check if the buy order quantity is zero
                        db.session.delete(buy_order) 
                    if sell_order.quantity == 0: #check if the sell order quantity is zero
                        db.session.delete(sell_order) 

                    db.session.commit()  #commit the transaction          


