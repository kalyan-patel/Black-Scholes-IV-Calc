import numpy as np
from scipy.stats import norm

class BlackScholesModel:
    
    # Initialize the pricing model with all necessary parameters
    def __init__(self, S, K, T, r, sig):
        self.S = S              # Spot price
        self.K = K              # Strike price
        self.T = T              # Time to maturity
        self.r = r              # Risk-free rate
        self.sig = sig          # Volatility

    # Calculates the value of "d1" used in the BS formula
    def d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sig ** 2) * self.T) / (self.sig * np.sqrt(self.T))
    
    # Calculates the value of "d2" used in the BS formula
    def d2(self):
        return self.d1() - self.sig * np.sqrt(self.T)
    
    # Calculates the price of a call option given the current inputs
    def call_price(self):
        return self.S * norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2())
    
    # Calculates the price of a put option given the current inputs
    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1())

    # Uses the Newton-Raphson method to iteratively estimate the option's implied volatility
    def implied_volatility(self, option_price, tol=1e-8, max_iterations=100):
        sig = 0.5
        for i in range(max_iterations):
            self.sig = sig
            price = self.call_price()
            vega = self.S * norm.pdf(self.d1()) * np.sqrt(self.T)
            price_diff = option_price - price
            
            if abs(price_diff) < tol:
                return sig
                
            sig += price_diff / vega 
        
        return sig  # Return closest guess if max_iterations has been exceeded