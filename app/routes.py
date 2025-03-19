from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_from_directory #import Flask modules for web app functionality 
from models import db, User, Order, Trade, Portfolio #import database models 
from auth import register_user, login_user #import authentication functions
from app.monte_carlo.option_pricing import price_option #import option pricing function
from werkzeug.security import generate_password_hash, check_password_hash #import security functions
from trading import match_orders #import trading logic for order matching
from forms_1 import RegistrationForm, LoginForm #import form handling for user registration and login
from flask_login import login_user, logout_user, login_required, current_user #import flask_login for user sessions management
from app.monte_carlo.monte_carlo import monte_carlo_greeks, monte_carlo_price #import Monte Carlo simulation functions
import yfinance as yf #import Yahoo Finance API for retrieving financial data
from datetime import datetime #import datetime for handling time-based operations
from sqlalchemy import or_ #import SQLAlchemy ORM for database operations

#----- Create a Blueprint for modularity -----
routes = Blueprint('routes', __name__, static_folder='static') #allows structuring the app into reusable components

@routes.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm() #create an instance of the registration form
    if form.validate_on_submit(): #check if the form is submitted and valid
        new_user = User(username=form.username.data) #create a new user with the provided username
        new_user.set_password(form.password.data) #set the user's password
        new_user.set_email(form.email.data) #set the user's email
        new_user.balance = 10000 #initialise the user's balance to 10000
        db.session.add(new_user) #add the new user to the database session
        db.session.commit() #commit the session to save the user to the database
        flash('Registration successful! You can now start hustling', 'success') #flash a success message
        return redirect(url_for('routes.login')) #redirect to the login page
    return render_template('register.html', form=form) #render the registration template with the form

@routes.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route") #print a debug message for the login route
    if current_user.is_authenticated: #check if the current user is already authenticated
        print("Current user authenticated") #print a debug message if the user is authenticated
        return redirect(url_for('routes.home')) #redirect to the home page
    form = LoginForm() #create an instance of the login form
    if form.validate_on_submit(): #check if the form is submitted and valid
        print("Login validation successful") #print a debug message if the form validation is successful
        user = User.query.filter_by(email=form.email.data).first() #query the user by email
        if user and user.check_password(form.password.data): #check if the user exists and the password is correct
            login_user(user) #log the user in
            flash('Login successful!', 'success') #flash a success message
            return redirect(url_for('routes.home')) #redirect to the home page
        else:
            flash('Invalid email or password', 'danger') #flash an error message if the login fails

    print("Login route - End") #print a debug message for the end of the login route
    return render_template('login.html', form=form, register=routes.register) #render the login template with the form

@routes.route('/place_order', methods=['POST'])
def place_order():
    if not current_user.is_authenticated: #check if the current user is not authenticated
        print("Current user not authenticated") #print a debug message if the user is not authenticated
        return redirect(url_for('routes.login')) #redirect to the login page
    
    order_data = request.get_json() #get the order data from the request
    print("Hello Tanuj-------------", order_data, current_user.id, current_user.username, current_user.email) #print debug information

    order = Order() #create a new order instance
    order.user_id = current_user.id #set the user ID for the order
    order.option_type = "Call" if order_data['Type'] == "Call" else "Put" #set the option type based on the order data
    order.order_type = "BUY" if order_data['Trade_type'] == "BUY" else "SELL" #set the order type based on the order data
    order.price = order_data['Ask'] #set the order price
    order.quantity = order_data['Volume'] #set the order quantity
    order.stock_name = order_data['StockSymbol'] #set the stock name for the order
    order.timestamp = datetime.now() #set the current timestamp for the order
    db.session.add(order) #add the order to the database session
    db.session.commit() #commit the session to save the order to the database
    match_orders() #call the function to match orders
    return jsonify({"success": 200}), 200 #return a success response

@routes.route('/match_orders', methods=['POST'])
def run_order_matching():
    trades = match_orders() #call the function to match orders and get the trades
    return jsonify({"message": f"{len(trades)} trades executed"}), 200 #return a response with the number of trades executed

@routes.route('/')
def home():
    print("Static Folder Path:", routes.static_folder) #print the static folder path for debugging
    if current_user.is_authenticated: #check if the current user is authenticated
        print("Current user authenticated") #print a debug message if the user is authenticated
        return render_template('index.html') #render the home page template
    
    return redirect(url_for('routes.login')) #redirect to the login page if the user is not authenticated

@routes.route('/trade', methods=['GET', 'POST'])
def trade():
    if request.method == 'POST': #check if the request method is POST
        return jsonify({'message': 'Trade executed successfully'}) #return a success message for trade execution
    return render_template('trade.html') #render the trade page template

@routes.route('/portfolio')
def portfolio():
    if not current_user.is_authenticated: #check if the current user is not authenticated
        print("Current user not authenticated") #print a debug message if the user is not authenticated
        return redirect(url_for('routes.login')) #redirect to the login page

    user = User.query.filter_by(id=current_user.id).first() #query the user by ID
    available_funds = user.balance #get the user's available funds

    options = Portfolio.query.filter_by(user_id=current_user.id).all() #fetch the user's portfolio data
    print("Portfolio") #print a debug message for the portfolio route
    if options: #check if there are options in the portfolio
        for option in options: #iterate through the options
            print(option.stock_name, option.value) #print the stock name and value for each option
            return render_template('portfolio.html', stocks=options, available_funds=available_funds) #render the portfolio template with the options and available funds
    else:
        return render_template('portfolio.html', available_funds=available_funds) #render the portfolio template with only the available funds

@routes.route('/market-trends')
def market_trends():
    return render_template('market_trends.html') #render the market trends page template

@routes.route('/mc_greeks', methods=['GET', 'POST'])
def calculate_mc_greeks():
    return render_template('mc_greeks.html') #render the Monte Carlo Greeks calculation page template

@routes.route('/mc_greeks_calc', methods=['GET', 'POST'])
def calculate_mc_greeks_calc():
    data = request.json #get the data from the request
    initial_stock_price = float(data['initial_stock_price']) #get the initial stock price from the data
    K = float(data['K']) #get the strike price from the data
    T = float(data['T']) #get the time to expiry from the data
    r = float(data['r']) #get the risk-free rate from the data
    sigma = float(data['sigma']) #get the volatility from the data
    option_type = data['option_type'] #get the option type from the data

    greeks = monte_carlo_greeks(initial_stock_price=initial_stock_price, K=K, T=T, r=r, sigma=sigma, option_type=option_type) #calculate the Greeks using Monte Carlo simulation
    price = monte_carlo_price(initial_stock_price, K, T, r, sigma, option_type) #calculate the option price using Monte Carlo simulation

    greeks = jsonify({
        "greeks": greeks, 
        "option_price": price
    }) #create a JSON response with the Greeks and option price
    return greeks #return the JSON response

@routes.route('/options', methods=['GET', 'POST'])
def get_options():
    print("get_options") #print a debug message for the get_options route
    symbol = request.args.get('symbol', 'AAPL') #get the stock symbol from the request, default to AAPL if not provided
    try:
        stock = yf.Ticker(symbol) #get the stock data from Yahoo Finance
        expirations = stock.options #get the available expiration dates
        options_chain = {} #initialise an empty dictionary for the options chain

        for exp in expirations[:2]: #fetch only the first two expiration dates for efficiency
            calls = stock.option_chain(exp).calls.fillna(0) #get the call options and fill NaN values with 0
            puts = stock.option_chain(exp).puts.fillna(0) #get the put options and fill NaN values with 0
            options_chain[exp] = {
                "calls": calls.to_dict(orient="records"),
                "puts": puts.to_dict(orient="records")
            } #add the call and put options to the options chain
        
        return jsonify({
            "symbol": symbol,
            "expirations": expirations,
            "options_chain": options_chain
        }) #return a JSON response with the options chain
    except Exception as e:
        return jsonify({"error": str(e)}), 500 #return an error response if an exception occurs

@routes.route('/order_history', methods=['GET', 'POST'])
def order_history():
    if not current_user.is_authenticated: #check if the current user is not authenticated
        return 'OK' #return a simple response if the user is not authenticated

    orders = Order.query.filter(Order.user_id == current_user.id).all() #fetch the user's order history

    return render_template('order_history.html', orders=orders) #render the order history template with the orders

@routes.route('/trade_history', methods=['GET', 'POST'])
def trade_history():
    if not current_user.is_authenticated: #check if the current user is not authenticated
        return 'OK' #return a simple response if the user is not authenticated

    trades = Trade.query.filter(or_(Trade.buyer_id == current_user.id, Trade.seller_id == current_user.id)).all() #fetch the user's trade history
    for trade in trades: #iterate through the trades
        trade.order_type = "BUY" if trade.buyer_id == current_user.id else "SELL" #set the order type based on the user ID
        trade.value = trade.quantity * trade.price #calculate the trade value

    return render_template('trade_history.html', trades=trades) #render the trade history template with the trades

@routes.route('/learn')
def learn():
    return render_template('learn.html') #render the learn page template

if __name__ == '__main__':
    routes.run(debug=True) #run the Flask app in debug mode

