import backtrader as bt

class MovingAverageCrossover(bt.Strategy):
    params = (
        ('short_period', 50),  # Short-term moving average period
        ('long_period', 200),  # Long-term moving average period
    )
    
    def __init__(self):
        # Define the short and long moving averages
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
        
        # Create a crossover signal (1 for buy, -1 for sell)
        self.cross_over = bt.indicators.CrossOver(self.sma_short, self.sma_long)

    def next(self):
        if self.cross_over > 0:  # Buy signal: short crosses above long
            if not self.position:  # If not in position
                self.buy()
        elif self.cross_over < 0:  # Sell signal: short crosses below long
            if self.position:  # If in position
                self.sell()
