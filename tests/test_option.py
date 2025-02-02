import pytest
from app.monte_carlo.option_pricing import price_option

def test_price_option_correctness():
    IS = 100
    ER = 0.05
    sigma = 0.2
    T = 1
    K = 110
    timesteps = 365
    simulations = 100000
    option_type = 'call'

    result = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type)
    assert result > 0
    assert isinstance(result, float)

#validation against expected values using Black-Scholes model
def test_against_black_scholes():
    from app.monte_carlo.option_pricing import price_option
    from app.black_scholes import black_scholes_price  # Hypothetical function

    # Define parameters
    IS = 100
    ER = 0.05
    sigma = 0.2
    T = 1
    K = 110
    timesteps = 365
    simulations = 100000
    option_type = 'call'

    # Calculate using Monte Carlo
    monte_carlo_price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type)

    # Calculate using Black-Scholes
    bs_price = black_scholes_price(IS, ER, sigma, T, K, option_type)

    # Validate the results (Monte Carlo should be close to Black-Scholes for high simulations)
    assert abs(monte_carlo_price - bs_price) / bs_price < 0.05  # Allow 5% deviation

#testing edge cases
def test_edge_cases():
    from app.monte_carlo.option_pricing import price_option

    # Extreme volatility
    assert price_option(100, 0.05, 2.0, 1, 365, 10000, 110, 'call') > 0

    # Long time to maturity
    assert price_option(100, 0.05, 0.2, 10, 3650, 10000, 150, 'call') > 0

    # Very high strike price
    assert price_option(100, 0.05, 0.2, 1, 365, 10000, 1000, 'put') > 0

import matplotlib.pyplot as plt
from app.monte_carlo.visualise_gbm import geometric_brownian_motion