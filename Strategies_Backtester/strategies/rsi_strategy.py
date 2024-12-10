import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),      # RSI period
        ('rsi_overbought', 70),  # Overbought threshold
        ('rsi_oversold', 30),    # Oversold threshold
    )
    
    def __init__(self):
        # Define the RSI indicator
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
    
    def next(self):
        if self.rsi < self.params.rsi_oversold:  # Buy signal: RSI crosses below the oversold level
            if not self.position:  # If not in position
                self.buy()
        elif self.rsi > self.params.rsi_overbought:  # Sell signal: RSI crosses above the overbought level
            if self.position:  # If in position
                self.sell()
