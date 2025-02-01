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