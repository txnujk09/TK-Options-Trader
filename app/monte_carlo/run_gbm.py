from monte_carlo import geometric_brownian_motion

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
print(paths[0])