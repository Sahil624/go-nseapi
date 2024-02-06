import backtrader as bt
from strategies.base_strategy.base import TradePnlStrategy

class SmaCross(TradePnlStrategy):
    strategy_name = "SMA Crossover Strategy"
    strategy_description = "A simple moving average crossover strategy that buys when the short-term moving average crosses above the long-term moving average, and sells when it crosses below."
    favourable_conditions = "Best in trending markets where clear upward or downward trends are established."

    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        super().next()
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position