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
