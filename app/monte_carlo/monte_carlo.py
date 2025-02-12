import sys #imports the sys module
import numpy as np #imports the numpy library
import matplotlib.pyplot as plt #imports the pyplot module from matplotlib

#Simulates stock price paths using the Geometric Brownian Motion
def geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations): #defines the function
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
    for t in range(1, timesteps): #starts at t=1 and runs until t=timesteps-1
        paths[:, t] = paths[:, t-1] * np.exp((ER - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * random_factors[:, t-1]) #discretised form of the geometric brownian motion
  
    return paths

def run_gbm(): #defines the run_gbm function
    # Parameters
    IS = 100
    ER = 0.05
    sigma = 0.2
    T = 1
    timesteps = 100
    simulations = 10

    #calls the geometric_brownian_motion function and stores the generated stock price simulations in variable paths
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations) 

    # Print the first simulation
    print("Simulated Stock Price Paths (First Simulation):")
    print(paths)

def run_gbm_visual(): #defines the run_gbm_visual function
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
    plt.figure(figsize=(10, 6)) #creates new figure with size of (10,6) inches
    for path in paths: #loops through each simulated stock price path stored in paths 
        plt.plot(path) #plot each path as a separate line on graph
    plt.title("Simulated Stock Price Paths (Geometric Brownian Motion)") #adds a title for clarity
    plt.xlabel("Time Steps") #x label for clarity
    plt.ylabel("Stock Price") #y label for clarity
    plt.grid() #enables the grid to make it easier to analyse trends
    plt.show() #displays to plot

#ensures the script runs only when executed directly
if __name__ == "__main__":
    sys.exit(run_gbm_visual()) #calls the run_gbm_visual function which generates and visualises GBM simulations
#sys.exit() ensures clean program termination after execution