import backtrader as bt

class BollingerBands(bt.Strategy):
    params = (
        ('bb_period', 20),     # Period for the Bollinger Bands
        ('bb_dev', 2),         # Number of standard deviations for the bands
    )
    
    def __init__(self):
        # Define the Bollinger Bands
        self.boll = bt.indicators.BollingerBands(self.data.close,
                                                 period=self.params.bb_period,
                                                 devfactor=self.params.bb_dev)
        
    def next(self):
        if self.data.close[0] < self.boll.bot[0]:  # Buy signal: price crosses below lower band
            if not self.position:  # If not in position
                self.buy()
        elif self.data.close[0] > self.boll.top[0]:  # Sell signal: price crosses above upper band
            if self.position:  # If in position
                self.sell()
