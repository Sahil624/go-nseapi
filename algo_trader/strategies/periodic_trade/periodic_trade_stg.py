import backtrader as bt
import pandas as pd
from strategies.base_strategy.base import TradePnlStrategy

class PeriodicTradeStrategy(TradePnlStrategy):    
    strategy_name = "Periodic Trade Strategy"
    strategy_description = "A strategy that periodically buys and sells assets based on fixed intervals."
    favourable_conditions = "Works in stable or oscillating markets where periodic price movements can be anticipated."

    params = dict(
        buy_interval=10,  # number of bars to wait before buying again
        sell_interval=30  # number of bars to wait before selling again
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buy_counter = 0
        self.sell_counter = 0

    def next(self):
        super().next()  # Call the base class next method
        self.buy_counter += 1
        self.sell_counter += 1

        if not self.getposition():  # not in the market
            if self.buy_counter >= self.p.buy_interval:
                self.buy()
                self.buy_counter = 0  # reset the counter after buying

        elif self.getposition():  # in the market
            if self.sell_counter >= self.p.sell_interval:
                self.sell()
                self.sell_counter = 0  # reset the counter after selling