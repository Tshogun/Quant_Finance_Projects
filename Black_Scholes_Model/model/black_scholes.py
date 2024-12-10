import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, S0, K, T, r, sigma):
        """
        Initialize the Black-Scholes model with input parameters.
        
        Parameters:
        S0      : Current stock price (spot price)
        K       : Strike price
        T       : Time to maturity (in years)
        r       : Risk-free interest rate (annual)
        sigma   : Volatility (annual)
        """
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _calculate_d1(self):
        """Calculate d1 in the Black-Scholes formula."""
        return (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))

    def _calculate_d2(self, d1):
        """Calculate d2 in the Black-Scholes formula."""
        return d1 - self.sigma * np.sqrt(self.T)

    def calculate_call_price(self):
        """Calculate the theoretical price of a European call option."""
        d1 = self._calculate_d1()
        d2 = self._calculate_d2(d1)
        call_price = (self.S0 * norm.cdf(d1)) - (self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        return call_price

    def calculate_put_price(self):
        """Calculate the theoretical price of a European put option."""
        d1 = self._calculate_d1()
        d2 = self._calculate_d2(d1)
        put_price = (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) - (self.S0 * norm.cdf(-d1))
        return put_price

# Example of usage
if __name__ == "__main__":
    # Initialize with parameters
    S0 = 100       # Spot price of the stock
    K = 100        # Strike price of the option
    T = 1          # Time to maturity (1 year)
    r = 0.05       # Risk-free interest rate (5%)
    sigma = 0.2    # Volatility (20%)

    # Create Black-Scholes object
    option = BlackScholes(S0, K, T, r, sigma)

    # Calculate call and put prices
    call_price = option.calculate_call_price()
    put_price = option.calculate_put_price()

    print(f"Call Option Price: {call_price:.2f}")
    print(f"Put Option Price: {put_price:.2f}")
