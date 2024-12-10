import backtrader as bt

class MACDCrossover(bt.Strategy):
    params = (
        ('macd_fast', 12),  # Fast period for MACD
        ('macd_slow', 26),  # Slow period for MACD
        ('macd_signal', 9), # Signal period for MACD
    )
    
    def __init__(self):
        # Initialize the MACD and signal line
        self.macd = bt.indicators.MACD(self.data.close,
                                       fastperiod=self.params.macd_fast,
                                       slowperiod=self.params.macd_slow,
                                       signalperiod=self.params.macd_signal)
        
        # Create a crossover signal (1 for buy, -1 for sell)
        self.cross_over = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if self.cross_over > 0:  # Buy signal: MACD crosses above the signal line
            if not self.position:  # If not in position
                self.buy()
        elif self.cross_over < 0:  # Sell signal: MACD crosses below the signal line
            if self.position:  # If in position
                self.sell()
