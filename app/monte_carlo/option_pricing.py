import numpy as np
from monte_carlo import geometric_brownian_motion

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

    print(f"Call Option Price: {call_price:.2f}")
    print(f"Put Option Price: {put_price:.2f}")

if __name__ == "__main__":
    run_price_option()