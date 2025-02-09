import sys
import numpy as np
import matplotlib.pyplot as plt

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

def run_gbm():
    # Parameters
    IS = 100
    ER = 0.05
    sigma = 0.2
    T = 1
    timesteps = 100
    simulations = 10

    # Run GBM simulation
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)

    # Print the first simulation
    print("Simulated Stock Price Paths (First Simulation):")
    print(paths)

def run_gbm_visual():
    # Parameters for GBM
    IS = 100  # Initial stock price
    ER = 0.05  # Expected return (drift)
    sigma = 0.2  # Volatility
    T = 1  # Time period in years
    timesteps = 100  # Number of time steps
    simulations = 10  # Number of simulated paths

    # Simulate GBM paths
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)

    # Plot the simulated paths
    plt.figure(figsize=(10, 6))
    for path in paths:
        plt.plot(path)
    plt.title("Simulated Stock Price Paths (Geometric Brownian Motion)")
    plt.xlabel("Time Steps")
    plt.ylabel("Stock Price")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    sys.exit(run_gbm_visual())