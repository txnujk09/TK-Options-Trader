from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, User, Order, Trade
from auth import register_user, login_user
from app.monte_carlo.option_pricing import price_option
from werkzeug.security import generate_password_hash, check_password_hash
from trading import match_orders
from forms_1 import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from app.monte_carlo.monte_carlo import monte_carlo_greeks

routes = Blueprint('routes', __name__)

@routes.route('/price_option', methods=['POST'])
def calculate_option_price():
    data = request.get_json()
    try:
        IS = data.get('IS')
        ER = data.get('ER')
        sigma = data.get('sigma')
        T = data.get('T')
        timesteps = data.get('timesteps')
        simulations = data.get('simulations')
        K = data.get('K')
        option_type = data.get('option_type')

        if not all([IS, ER, sigma, T, timesteps, simulations, K, option_type]):
            return jsonify({"error": "Missing required parameters"}), 400

        price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type)
        return jsonify({"option_price": price}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

# User login
#@routes.route('/login', methods=['POST'])
#def login():
#    data = request.json
#    user = User.query.filter_by(username=data['username']).first()
#    if user and check_password_hash(user.password, data['password']):
#       return jsonify({'message': 'Login successful!'})
#    return jsonify({'message': 'Invalid credentials'}), 401

@routes.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    
    form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user)
    #         flash('Login successful!', 'success')
    #         return redirect(url_for('dashboard'))
    #     else:
    #         flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

#Flask API routes for placing orders and executing trades
main = Blueprint("main", __name__)

@main.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    new_order = Order(
        user_id=data["user_id"],
        option_id=data["option_id"],
        order_type=data["order_type"],
        quantity=data["quantity"],
        price=data["price"],
        status="pending"
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully"}), 200

@main.route('/match_orders', methods=['POST'])
def run_order_matching():
    trades = match_orders()
    return jsonify({"message": f"{len(trades)} trades executed"}), 200

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/trade', methods=['GET', 'POST'])
def trade():
    if request.method == 'POST':
        # Handle trade execution logic here
        return jsonify({'message': 'Trade executed successfully'})
    return render_template('trade.html')

@routes.route('/portfolio')
def portfolio():
    # Fetch portfolio data for display
    return render_template('portfolio.html')

@routes.route('/market-trends')
def market_trends():
    # Fetch market trends data for visualisation
    return render_template('market_trends.html')

#provides an API for users to compute Greeks
@routes.route('/calculate_mc_greeks', methods=['POST'])
def calculate_mc_greeks():

    data = request.json
    S = float(data['S'])  # Stock price
    K = float(data['K'])  # Strike price
    T = float(data['T'])  # Time to expiry in years
    r = float(data['r'])  # Risk-free rate
    sigma = float(data['sigma'])  # Volatility
    option_type = data['option_type']  # "call" or "put"

    greeks = monte_carlo_greeks(S, K, T, r, sigma, option_type)

    return render_template('mc_greeks.html', greeks=greeks)
    
    