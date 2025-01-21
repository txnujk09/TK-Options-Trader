from monte_carlo.monte_carlo import geometric_brownian_motion

def test_gbm_output_shape():
    """
    Test if the GBM function returns the correct output shape.
    """
    IS, ER, sigma, T, timesteps, simulations = 100, 0.05, 0.2, 1, 100, 1000
    paths = geometric_brownian_motion(IS, ER, sigma, T, timesteps, simulations)
    assert paths.shape == (simulations, timesteps), f"Expected shape {(simulations, timesteps)}, got {paths.shape}"