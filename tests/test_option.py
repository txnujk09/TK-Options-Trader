import pytest
import sys
import os
# Add the root directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/monte_carlo')))

from app.monte_carlo.option_pricing import price_option

def test_price_option_correctness():
    """
    Unit test for the 'price_option' function to ensure it returns a valid option price
    """
    #define parameters
    IS = 100 #initial stock price
    ER = 0.05 #expected return
    sigma = 0.2 #volatility
    T = 1 #time to maturity (yrs)
    K = 110 #strike price
    timesteps = 365 #no. of discrete time steps
    simulations = 100000 #no. of monte carlo simulations
    option_type = 'call' #type of option

    result = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type) #run option pricing function
    assert result > 0,"Option price should be >0" #check option price is positive
    assert isinstance(result, float), "Option price should be a float" #checks option price is a float

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
    from app.monte_carlo.option_pricing import price_option #importing the function to be tested

    #extreme volatility (sigma=2.0)
    assert price_option(100, 0.05, 2.0, 1, 365, 10000, 110, 'call') > 0 #option price should be >0

    #long time to maturity (T=10yrs)
    assert price_option(100, 0.05, 0.2, 10, 3650, 10000, 150, 'call') > 0 #option price should be >0

    #very high strike price (K=1000, much greater than stock price 100)
    assert price_option(100, 0.05, 0.2, 1, 365, 10000, 1000, 'call') < 1 #option price should be <1

    #very low strike price (K=1, much lower than stock price 100)
    assert (price_option(100, 0.05, 0.2, 1, 365, 10000, 1, 'call')-99)<5 #option price should be <5

    