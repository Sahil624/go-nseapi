from datetime import datetime
import json
import backtrader as bt
import pandas as pd
import numpy as np

from api.backtest.model import Backtest, BacktestIteration

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class TradePnlStrategy(bt.Strategy):
    # Metadata for the strategy
    strategy_name = "Generic Strategy"
    strategy_description = "This is a generic trading strategy."
    favourable_conditions = "Favourable under various market conditions."


    backtest: Backtest = None
    params = (
        ('backtest_obj', None),
        ('is_enabled', True),
    )

    def __init__(self, params=None):
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)

        self.trades = []
        self.backtest = self.p.backtest_obj

    def notify_trade(self, trade: bt.Trade):

        if trade.isclosed:
            trade_info = {
                # 'entry_date': trade.data.datetime.date(trade.baropen),
                'entry_date': trade.open_datetime(),
                'entry_price': trade.price,
                # 'exit_date': trade.data.datetime.date(trade.barclose),
                'exit_date':trade.close_datetime(),
                'exit_price': trade.price,
                'size': trade.size,
                'direction': 'long' if trade.size > 0 else 'short',
                'profit': trade.pnl,
                'commission': trade.commission,
                'duration': trade.barclose - trade.baropen
            }
            self.trades.append(trade_info)
            # Save trade to the database
            BacktestIteration.create(
                backtest_id=self.backtest.id,
                symbol=trade.data._name,
                entry_date=trade_info['entry_date'],
                entry_price=trade_info['entry_price'],
                exit_date=trade_info['exit_date'],
                exit_price=trade_info['exit_price'],
                size=trade_info['size'],
                direction=trade_info['direction'],
                profit=trade_info['profit'],
                commission=trade_info['commission'],
                duration=trade_info['duration']
            )

    def get_trade_statistics(self) -> str:
        if not self.trades:
            return ''

        df = pd.DataFrame(self.trades)
        stats = {
            'AvgEntryPrice': df['entry_price'].mean(),  # Average entry price of all trades
            'AvgExitPrice': df['exit_price'].mean(),  # Average exit price of all trades
            'AvgMktTime': df['duration'].mean(),  # Average duration (time in market) of all trades
            'BL': df[df['profit'] < 0]['profit'].sum(),  # Total loss from losing trades
            'BP': df[df['profit'] > 0]['profit'].sum(),  # Total profit from winning trades
            'CalmerRatio': self._calmar_ratio(df),  # Calmar ratio (annual return / max drawdown)
            'LFP': df[df['profit'] < 0]['profit'].max(),  # Largest financial loss in a single trade
            'LLT': df[df['profit'] < 0]['duration'].max(),  # Longest losing trade duration
            'LS': df[df['profit'] < 0]['size'].count(),  # Number of losing trades
            'LWT': df[df['profit'] > 0]['duration'].max(),  # Longest winning trade duration
            'Loss': df[df['profit'] < 0]['size'].count(),  # Number of losing trades (duplicate of LS)
            'MLP': df[df['profit'] < 0]['profit'].mean(),  # Mean loss per losing trade
            'MLV': df['profit'].min(),  # Maximum loss value in a single trade
            'MPP': df[df['profit'] > 0]['profit'].mean(),  # Mean profit per winning trade
            'MPV': df['profit'].max(),  # Maximum profit value in a single trade
            'MTTR': df['duration'].mean(),  # Mean time to recovery (average trade duration)
            'MTTREnd': str(df['exit_date'].max()),  # End date of the latest trade
            'MTTRStart': str(df['entry_date'].min()),  # Start date of the earliest trade
            'MaxDD': self._max_drawdown(df),  # Maximum drawdown (largest drop from peak)
            'MaxDDV': df['profit'].min(),  # Maximum drawdown value
            'MaxSharpRatio': self._sharpe_ratio(df),  # Maximum Sharpe ratio
            'MinDD': 0,  # Minimum drawdown (zero as a placeholder)
            'MinDDV': df['profit'].max(),  # Minimum drawdown value (peak profit)
            'PnL': df['profit'].sum(),  # Total profit and loss
            'Signal': len(df),  # Number of signals/trades
            'Timestamp': str(datetime.now().timestamp()),  # Timestamp of the calculation
            'WS': df[df['profit'] > 0]['size'].count(),  # Number of winning trades
            'Wins': df[df['profit'] > 0]['size'].count()  # Number of winning trades (duplicate of WS)
        }

        return json.dumps(stats, cls=NpEncoder)

    def _calmar_ratio(self, df):
        annual_return = df['profit'].sum() / len(df) * 252  # 252 trading days in a year
        max_dd = self._max_drawdown(df)
        return annual_return / abs(max_dd) if max_dd != 0 else 0

    def _max_drawdown(self, df):
        cumulative = df['profit'].cumsum()
        peak = cumulative.cummax()
        drawdown = cumulative - peak
        return drawdown.min()

    def _sharpe_ratio(self, df, risk_free_rate=0):
        return (df['profit'].mean() - risk_free_rate) / df['profit'].std() * (252 ** 0.5) if df['profit'].std() != 0 else 0

    @classmethod
    def get_metadata(cls):
        return {
            'strategy_name': cls.strategy_name,
            'strategy_description': cls.strategy_description,
            'favourable_conditions': cls.favourable_conditions
        }