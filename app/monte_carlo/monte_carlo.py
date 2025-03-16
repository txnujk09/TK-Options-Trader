import sys #imports the sys module
import numpy as np #imports the numpy library and assigns it the alias np
import matplotlib.pyplot as plt #imports the pyplot module from matplotlib

#Simulates stock price paths using the Geometric Brownian Motion
def geometric_brownian_motion(initial_stock_price, ER, sigma, T, timesteps, simulations): #defines the function
    """
    Parameters:
     initial_stock_price (float): Intial stock price
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
    paths[:, 0] = initial_stock_price

    #generate paths using the GBM formula
    for t in range(1, timesteps): #starts at t=1 and runs until t=timesteps-1
        paths[:, t] = paths[:, t-1] * np.exp((ER - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * random_factors[:, t-1]) #discretised form of the geometric brownian motion
  
    return paths

def run_gbm(): #defines the run_gbm function
    # Parameters
    initial_stock_price = 100
    ER = 0.05
    sigma = 0.2
    T = 1
    timesteps = 100
    simulations = 10

    #calls the geometric_brownian_motion function and stores the generated stock price simulations in variable paths
    paths = geometric_brownian_motion(initial_stock_price, ER, sigma, T, timesteps, simulations) 

    # Print the first simulation
    print("Simulated Stock Price Paths (First Simulation):")
    print(paths)

def run_gbm_visual(): #defines the run_gbm_visual function
    # Parameters for GBM
    initial_stock_price = 100  # Initial stock price
    ER = 0.05  # Expected return (drift)
    sigma = 0.2  # Volatility
    T = 1  # Time period in years
    timesteps = 100  # Number of time steps
    simulations = 10  # Number of simulated paths

    # Simulate GBM paths
    paths = geometric_brownian_motion(initial_stock_price, ER, sigma, T, timesteps, simulations)

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

def monte_carlo_price(initial_stock_price, K, T, r, sigma, option_type, num_simulations=10000):
    """Computes the option price using Monte Carlo simulation."""
    Z = np.random.standard_normal(num_simulations) #generates standard normal random numbers
    S_T = initial_stock_price * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z) #simulates the future stock price using the GBM
    if option_type == "call": #checks if the option initial_stock_price a call option
        payoffs = np.maximum(S_T - K, 0) #calculates the payoff for a European call option at expiration
    else: #the previous 'if' condition wasn't met so must be a put option
        payoffs = np.maximum(K - S_T, 0) #calculates the payoff for a European put option at expiration
    return np.exp(-r * T) * np.mean(payoffs) #discounts the expected payoff for option price

def monte_carlo_greeks(initial_stock_price, K, T, r, sigma, option_type, num_simulations=10000, epsilon=1e-4):
    """
    Computes option Greeks using the Monte Carlo method.

    Parameters:
    initial_stock_price (float)          : Current stock price
    K (float)          : Strike price
    T (float)          : Time to maturity (years)
    r (float)          : Risk-free interest rate
    sigma (float)      : Volatility of the underlying asset
    option_type (str)  : "call" or "put"
    num_simulations (int): Number of Monte Carlo simulations
    epsilon (float)    : Small perturbation for numerical differentiation

    Returns:
    dict: Contains Delta, Gamma, Vega, Theta, and Rho
    """

    # Base option price
    base_price = monte_carlo_price(initial_stock_price, K, T, r, sigma, option_type) #calls the monte_carlo_price function which computes the option price

    # Delta (∂C/∂S): Sensitivity to stock price
    delta_price_up = monte_carlo_price(initial_stock_price + epsilon, K, T, r, sigma, option_type) #recalculates option price with slightly higher stock price
    delta_price_down = monte_carlo_price(initial_stock_price - epsilon, K, T, r, sigma, option_type) #recalculates option price with slightly lower stock price
    delta = (delta_price_up - delta_price_down) / (2 * epsilon) #computes the gradient of the option price with respect to the stock price

    # Gamma (∂²C/∂S²): Sensitivity of Delta
    gamma = (delta_price_up - 2 * base_price + delta_price_down) / (epsilon ** 2) #calculated using the second-order finite difference approximation

    # Vega (∂C/∂σ): Sensitivity to volatility
    vega_price_up = monte_carlo_price(initial_stock_price, K, T, r, sigma + epsilon, option_type) #recalculates the option price with higher volatility
    vega_price_down = monte_carlo_price(initial_stock_price, K, T, r, sigma - epsilon, option_type) #recalculates the option price with lower volatility
    vega = (vega_price_up - vega_price_down) / (2 * epsilon) #computes the gradient of the option price with respect to the volatility of the underlying asset

    # Theta (∂C/∂T): Sensitivity to time
    theta_price_up = monte_carlo_price(initial_stock_price, K, T + epsilon, r, sigma, option_type) #recalculates the option price with more time remaining
    theta_price_down = monte_carlo_price(initial_stock_price, K, T - epsilon, r, sigma, option_type) #recalculates the option price with less time remaining
    theta = (theta_price_down - theta_price_up) / (2 * epsilon) #computes the rate of decay in option value

    # Rho (∂C/∂r): Sensitivity to interest rate
    rho_price_up = monte_carlo_price(initial_stock_price, K, T, r + epsilon, sigma, option_type) #recalculates the option price with a higher risk-free rate
    rho_price_down = monte_carlo_price(initial_stock_price, K, T, r - epsilon, sigma, option_type) #recalculates the option price with a lower risk-free rate
    rho = (rho_price_up - rho_price_down) / (2 * epsilon) #computes the sensitivity to interest rate

    #returns the computed Greeks in a dictionary format
    return {
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega,
        "Theta": theta,
        "Rho": rho
    }

# Example usage with dummy values
greeks = monte_carlo_greeks(initial_stock_price=100, K=105, T=1, r=0.05, sigma=0.2, option_type="call")
"""
Sample values:
initial_stock_price=100: Stock price initial_stock_price $100
K=105: Strike price initial_stock_price $105
T=1: One year to expiration
r=0.05: Risk-free interest rate initial_stock_price 5%
sigma=0.2: 20% volatility
option_type="call": pricing a call option

"""
print(greeks) #print the computed Greeks
