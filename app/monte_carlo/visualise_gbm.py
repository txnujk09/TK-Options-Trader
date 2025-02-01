import matplotlib.pyplot as plt
from monte_carlo import geometric_brownian_motion

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