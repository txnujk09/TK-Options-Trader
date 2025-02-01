from app.monte_carlo.monte_carlo import geometric_brownian_motion

def test_gbm_output_shape():
    """
    Test if the GBM function returns the correct output shape.
    """
    IS, ER, sigma, T, timesteps, simulations = 100, 0.05, 0.2, 1, 100, 1000
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)
    assert paths.shape == (simulations, timesteps), f"Expected shape {(simulations, timesteps)}, got {paths.shape}"

def test_gbm_non_negative_prices():
    """
    Test that GBM never produces negative stock prices.
    """
    IS, ER, sigma, T, timesteps, simulations = 100, 0.05, 0.2, 1, 100, 1000
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)
    assert (paths >= 0).all(), "GBM produced negative stock prices"

def test_gbm_initial_price():
    """
    Test that the first column in GBM paths equals the initial stock price.
    """
    IS, ER, sigma, T, timesteps, simulations = 100, 0.05, 0.2, 1, 100, 1000
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)
    assert (paths[:, 0] == IS).all(), "Initial stock price mismatch in GBM paths"

def test_gbm_high_volatility():
    """
    Test GBM with very high volatility.
    """
    IS, ER, sigma, T, timesteps, simulations = 100, 0.05, 2.0, 1, 100, 1000
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)
    assert paths.shape == (simulations, timesteps), "Shape mismatch for high volatility"
    assert (paths >= 0).all(), "GBM produced negative prices with high volatility"