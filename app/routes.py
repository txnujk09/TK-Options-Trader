from flask import Blueprint, request, jsonify
from models import db, User
from auth import register_user, login_user
from monte_carlo.option_pricing import price_option
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return jsonify({"message": "Welcome to the Options Trading API!"})

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
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful!'})
    return jsonify({'message': 'Invalid credentials'}), 401


    
    