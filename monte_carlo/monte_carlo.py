import numpy as np

def geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations):
    dt = T / timesteps
    random_factors = np.random.normal(0, 1, (simulations, timesteps))
    paths = np.zeros((simulations, timesteps))
    paths[:, 0] = IS
    for t in range(1, timesteps):
        paths[:, t] = paths[:, t-1] * np.exp((ER - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * random_factors[:, t-1])
    return paths
