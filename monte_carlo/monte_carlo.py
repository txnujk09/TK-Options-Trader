import numpy as np

#Simulates stock price paths using the Geometric Brownian Motion
def geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations):
    """
    Parameters:
     IS (float): Intial stock price
     ER (float): Expected return (drift)
     sigma (float): Volatility of the stock
     T (float): Total time period (in years)
     timesteps (int): Number of time steps
     simulations (int): Number of simulated paths

    Return:
     np.ndarray: Simulated stock prices paths of shape (simulations, timesteps)
     
    """
    dt = T / timesteps #time step size
    #generate random normal values for simulations
    random_factors = np.random.normal(0, 1, (simulations, timesteps))
    #initalise the paths array
    paths = np.zeros((simulations, timesteps))
    #set the initial stock price for all simulations
    paths[:, 0] = IS

    #generate paths using the GBM formula
    for t in range(1, timesteps):
        paths[:, t] = paths[:, t-1] * np.exp((ER - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * random_factors[:, t-1])
    return paths
