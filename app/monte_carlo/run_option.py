from option_pricing import price_option

def main():
    IS = 100  # Initial stock price
    ER = 0.05  # Expected return
    sigma = 0.2  # Volatility
    T = 1  # Time to maturity
    timesteps = 100  # Number of time steps
    simulations = 1000  # Number of simulated paths
    K = 105  # Strike price

    # Calculate call and put prices
    call_price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type="call")
    put_price = price_option(IS, ER, sigma, T, timesteps, simulations, K, option_type="put")

    print(f"Call Option Price: {call_price:.2f}")
    print(f"Put Option Price: {put_price:.2f}")

if __name__ == "__main__":
    main()