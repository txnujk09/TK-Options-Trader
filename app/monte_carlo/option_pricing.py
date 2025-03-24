import numpy as np #imports the numpy library and assigns it the alias 'np'
from monte_carlo import geometric_brownian_motion #imports 'geometric_brownian_motion' from the module 'monte_carlo'

def price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type="call"):
    """
    Price a European option using Monte Carlo simulation.
    """
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations) #generate stock price paths
    S_T = paths[:, -1] #get the stock price at maturity

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0) #calculate the payoff for a call option
    elif option_type == "put":
        payoffs = np.maximum(K - S_T, 0) #calculate the payoff for a put option
    else:
        raise ValueError("Invalid option type. Choose 'call' or 'put'.")

    discounted_payoff = np.exp(-ER * T) * np.mean(payoffs) #calculate the discounted payoff
    print(discounted_payoff)
    return discounted_payoff

def run_price_option():
    IS = 100  # Initial stock price
    ER = 0.05  # Expected return
    sigma = 0.2  # Volatility
    T = 1  # Time to maturity
    timesteps = 100  # Number of time steps
    simulations = 1000  # Number of simulated paths
    K = 105  # Strike price

    # Calculate call and put prices
    call_price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type="call")
    put_price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type="put")

    print(f"Call Option Price: {call_price:.2f}") #print the call option price
    print(f"Put Option Price: {put_price:.2f}") #print the put option price

if __name__ == "__main__": 
    run_price_option() #run the run_price_option function