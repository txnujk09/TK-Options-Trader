import math
from scipy.stats import norm #import cumulative distribution function for normal distribution

def black_scholes_price(IS, r, sigma, T, K, option_type='call'):
    """
    Calculate the price of a European option using the Black-Scholes formula.

    Parameters:
    IS (float): initial stock price
    r (float): Risk-free rate
    sigma (float) Volatility of the stock
    T (float) Time to maturity (in years)
    K (float) Strike price
    option_type (str) 'call' or 'put'

    Returns:
    float : Option price
    """
    d1 = (math.log(IS / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T)) #calc d1 parameter used in Black-Scholes model
    d2 = d1 - sigma * math.sqrt(T) #calc d2 paramter, which is derived from d1

    #compute price based on whether option is call or put
    if option_type == 'call':
        #call option price formula
        return IS * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2) 
    elif option_type == 'put':
        #put option price formula
        return K * math.exp(-r * T) * norm.cdf(-d2) - IS * norm.cdf(-d1) 
    else:
        print("Invalid option type. Use 'call' or 'put'.") #print error message if option type is invalid