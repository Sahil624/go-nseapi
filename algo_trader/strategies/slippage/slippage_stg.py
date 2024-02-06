import backtrader as bt

from strategies.base_strategy.base import TradePnlStrategy

class SlippageStrategy(TradePnlStrategy):
    strategy_name = "Slippage Strategy"
    strategy_description = (
        "A strategy that incorporates slippage into a simple moving average crossover system. "
        "It buys when the short-term moving average crosses above the long-term moving average, "
        "and sells when it crosses below, considering a predefined slippage percentage."
    )
    favourable_conditions = (
        "Best in markets with moderate volatility where the impact of slippage can be realistically simulated. "
        "Less effective in highly volatile or low-liquidity markets where slippage might be unpredictable."
    )

    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30,  # period for the slow moving average
        slip_perc=0.005,  # slippage percentage,
    )

    def __init__(self, *args, **kwargs):
        super(SlippageStrategy, self).__init__(*args, **kwargs)
        sma1 = bt.indicators.SMA(period=self.p.pfast)
        sma2 = bt.indicators.SMA(period=self.p.pslow)
        self.crossover = bt.indicators.CrossOver(sma1, sma2)
        self.broker.set_slippage_perc(self.p.slip_perc)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()

    def notify_order(self, order):
        if order.status == order.Completed:
            super(SlippageStrategy, self).notify_order(order)
