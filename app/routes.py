from flask import Blueprint, request, jsonify
from monte_carlo.option_pricing import price_option

routes = Blueprint('routes', __name__)

@routes.route('/price_option', methods=['POST'])
def calculate_option_price():
    try:
        data = request.get_json()
        IS = data.get('IS')
        ER = data.get('ER')
        sigma = data.get('sigma')
        T = data.get('T')
        timesteps = data.get('timesteps')
        simulations = data.get('simulations')
        K = data.get('K')
        option_type = data.get('option_type')

        if not all([IS, ER, sigma, T, timesteps, simulations, K, option_type]):
            return jsonify({"error": "Missing one or more required parameters"}), 400
        if option_type not in ["call", "put"]:
            return jsonify({"error": "Invalid option_type. Choose 'call' or 'put'."}), 400

        price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type)
        return jsonify({"option_price": price}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@routes.route('/', methods=['get'])
def homepage():
    try:
        return jsonify({"option_price": "Tanuj Kakumani"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500