import numpy as np
from monte_carlo import geometric_brownian_motion

# #Simulates stock price paths using the Geometric Brownian Motion
# def geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations):
#     """
#     Parameters:
#      IS (float): Intial stock price
#      ER (float): Expected return (drift)
#      sigma (float): Volatility of the stock
#      T (float): Total time period (in years)
#      timesteps (int): Number of time steps
#      simulations (int): Number of simulated paths

#     Return:
#      np.ndarray: Simulated stock prices paths of shape (simulations, timesteps)
     
#     """
#     dt = T / timesteps #time step size
#     #generate random normal values for simulations
#     random_factors = np.random.normal(0, 1, (simulations, timesteps))
#     #initalise the paths array
#     paths = np.zeros((simulations, timesteps))
#     #set the initial stock price for all simulations
#     paths[:, 0] = IS

#     #generate paths using the GBM formula
#     for t in range(1, timesteps):
#         paths[:, t] = paths[:, t-1] * np.exp((ER - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * random_factors[:, t-1])
#     print(paths)    
#     return paths


def price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type="call"):
    """
    Price a European option using Monte Carlo simulation.
    """
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)
    S_T = paths[:, -1]

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - S_T, 0)
    else:
        raise ValueError("Invalid option type. Choose 'call' or 'put'.")

    discounted_payoff = np.exp(-ER * T) * np.mean(payoffs)
    print(discounted_payoff)
    return discounted_payoff


def main():
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

    print(f"Call Option Price: {call_price:.2f}")
    print(f"Put Option Price: {put_price:.2f}")

if __name__ == "__main__":
    main()