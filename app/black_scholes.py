import math
from scipy.stats import norm

def black_scholes_price(S, r, sigma, T, K, option_type='call'):
    """
    Calculate the price of a European option using the Black-Scholes formula.

    Parameters:
    S : float : Current stock price
    r : float : Risk-free rate
    sigma : float : Volatility of the stock
    T : float : Time to maturity (in years)
    K : float : Strike price
    option_type : str : 'call' or 'put'

    Returns:
    float : Option price
    """
    d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")