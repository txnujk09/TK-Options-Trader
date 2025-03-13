from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash #import Flask modules for web app functionality 
from models import db, User, Order, Trade, Portfolio #import database models 
from auth import register_user, login_user #import authentication functions
from app.monte_carlo.option_pricing import price_option #import option pricing function
from werkzeug.security import generate_password_hash, check_password_hash #import security functions
from trading import match_orders #import trading logic for order matching
from forms_1 import RegistrationForm, LoginForm #import form handling for user registration and login
from flask_login import login_user, logout_user, login_required, current_user #import flask_login for user sessions management
from app.monte_carlo.monte_carlo import monte_carlo_greeks 
import yfinance as yf #import Yahoo Finance API for retrieving financial data
from datetime import datetime #import datetime for handling time-based operations
from sqlalchemy import or_ #import SQLAlchemy ORM for database operations

#----- Create a Blueprint for modularity -----
routes = Blueprint('routes', __name__) #allows structuring the app into reusuable components

#----- API Route definition for Option Pricing -----
@routes.route('/option_pricing', methods=['GET', 'POST']) #define a GET/POST API endpoint
def calculate_option_price():
    try:
        return render_template('option_pricing.html')
    except Exception as e: #handle any unexpected errors and return an error message with status 500 (Internal Server Error)
        return jsonify({"error": str(e)}, 500)


#provides an API for users to compute Greeks
@routes.route('/option_price_calculate', methods=['GET', 'POST'])
def option_price_calculate():
    data = request.json
    print(data)
    IS = data.get('IS') #initial stock price
    ER = data.get('ER') #expected return
    sigma = data.get('sigma') #volatility of stock
    T = data.get('T') #time to maturity (in years)
    timesteps = data.get('timesteps') #no. of timesteps in simulation
    simulations = data.get('simulations') #no. of Monte Carlo simulation paths
    K = data.get('K') #strike price of option
    option_type = data.get('option_type') #type of option (i.e. 'call'/'put')

    #validate all required parameters are present
    if not all([IS, ER, sigma, T, timesteps, simulations, K, option_type]):
        print("Tanuj##")
        return jsonify({"error": "Missing required parameters"}, 400)

    #call Monte Carlo pricing function with extracted parameters
    print("Tanuj 1")
    price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type)

    return jsonify({"option_price": price}, 200) #return calculated option price as a JSON response with status 200 (OK)


@routes.route('/register', methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        new_user=User(username=form.username.data)
        new_user.set_password(form.password.data)
        new_user.set_email(form.email.data)
        new_user.balance=10000
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now start hustling', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route")
    if current_user.is_authenticated:
        print("Current user authenticated")
        return redirect(url_for('routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        print("Login validation successful")
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid email or password', 'danger')

    print("Login route - End")
    return render_template('login.html', form=form, register=routes.register)

@routes.route('/place_order', methods=['POST'])
def place_order():
    if not current_user.is_authenticated:
        print("Current user not authenticated")
        # User not authenticated, redirect to login
        return redirect(url_for('routes.login'))
    
    # Get order data
    order_data = request.get_json()
    print("Hello Tanuj-------------", order_data, current_user.id, current_user.username, current_user.email)

    order = Order()
    order.user_id = current_user.id
    order.option_type = "Call" if order_data['Type'] == "Call" else "Put"
    order.order_type = "BUY" if order_data['Trade_type'] == "BUY" else "SELL"
    order.price = order_data['Ask']
    order.quantity = order_data['Volume']
    order.stock_name = order_data['StockSymbol']
    order.timestamp = datetime.now()
    db.session.add(order)
    db.session.commit()
    match_orders()
    return jsonify({"success":200}), 200

@routes.route('/match_orders', methods=['POST'])
def run_order_matching():
    trades = match_orders()
    return jsonify({"message": f"{len(trades)} trades executed"}), 200

@routes.route('/')
def home():
    if current_user.is_authenticated:
        print("Current user authenticated")
        return render_template('index.html')
    
    return redirect(url_for('routes.login'))

@routes.route('/trade', methods=['GET', 'POST'])
def trade():
    if request.method == 'POST':
        # Handle trade execution logic here
        return jsonify({'message': 'Trade executed successfully'})
    return render_template('trade.html')


@routes.route('/portfolio')
def portfolio():
    if not current_user.is_authenticated:
        print("Current user not authenticated")
        # User not authenticated, redirect to login
        return redirect(url_for('routes.login'))

    user = User.query.filter_by(id=current_user.id).first()
    available_funds = user.balance

    # Fetch portfolio data for user id
    options = Portfolio.query.filter_by(user_id=current_user.id).all()
    print("Portfolio")
    if options:
        for option in options:
            print(option.stock_name, option.value)
            return render_template('portfolio.html', stocks=options, available_funds=available_funds)
    else:
        return render_template('portfolio.html', available_funds=available_funds)
    
@routes.route('/market-trends')
def market_trends():
    # Fetch market trends data for visualisation
    return render_template('market_trends.html')

#provides an API for users to compute Greeks
@routes.route('/mc_greeks', methods=['GET', 'POST'])
def calculate_mc_greeks():
    return render_template('mc_greeks.html')

    
#provides an API for users to compute Greeks
@routes.route('/mc_greeks_calc', methods=['GET', 'POST'])
def calculate_mc_greeks_calc():

    data = request.json
    S = float(data['S'])  # Stock price
    K = float(data['K'])  # Strike price
    T = float(data['T'])  # Time to expiry in years
    r = float(data['r'])  # Risk-free rate
    sigma = float(data['sigma'])  # Volatility
    option_type = data['option_type']  # "call" or "put"

    greeks = monte_carlo_greeks(S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type)

    greeks=jsonify({
            "greeks": greeks, 
            })
    return greeks

@routes.route('/options', methods=['GET', 'POST'])
def get_options():
    print("get_options")
    symbol = request.args.get('symbol', 'AAPL')  # Default to AAPL if no symbol provided
    try:
        stock = yf.Ticker(symbol)
        expirations = stock.options  # Get available expiration dates
        options_chain = {}

        for exp in expirations[:2]:  # Fetch only the first two expiration dates for efficiency
            calls = stock.option_chain(exp).calls.fillna(0)
            puts = stock.option_chain(exp).puts.fillna(0)
            options_chain[exp] = {
                "calls": calls.to_dict(orient="records"),
                "puts": puts.to_dict(orient="records")
            }
            
        return jsonify({
            "symbol": symbol,
            "expirations": expirations,
            "options_chain": options_chain
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/order_history', methods=['GET', 'POST'])
def order_history():
    if not current_user.is_authenticated:
        # User not authenticated, check what is best to return??
        return 'OK'

    orders = Order.query.filter(Order.user_id==current_user.id).all()

    return render_template('order_history.html', orders=orders)

@routes.route('/trade_history', methods=['GET', 'POST'])
def trade_history():
    if not current_user.is_authenticated:
        # User not authenticated, check what is best to return??
        return 'OK'

    trades = Trade.query.filter(or_(Trade.buyer_id==current_user.id,Trade.seller_id==current_user.id)).all()
    for trade in trades:
        trade.order_type = "BUY" if trade.buyer_id == current_user.id else "SELL"
        trade.value = trade.quantity * trade.price

    return render_template('trade_history.html', trades=trades)