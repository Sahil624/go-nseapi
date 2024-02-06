import logging
import os
import importlib
import sys
import backtrader as bt
from flask_jwt_extended import get_jwt_identity

from api.backtest.model import Analysis, Backtest
from data.manager import get_ohlc_data
from strategies.base_strategy.base import TradePnlStrategy
from typing import List, Tuple

# Function to dynamically import strategy module and get the strategy class
def get_strategy_class(module_name):
    module = importlib.import_module(module_name)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isinstance(attribute, type) and issubclass(attribute, bt.Strategy) and attribute is not bt.Strategy:
            return attribute
    return None

# Function to list all strategy files
def list_strategy_files(directory):
    strategy_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_stg.py'):
                strategy_files.append(os.path.join(root, file))
    return strategy_files

# Function to display menu and get user's choice
def display_menu(options):
    print("Select a strategy to backtest:")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    choice = int(input("Enter the number of the strategy: ")) - 1
    return options[choice]

# Main function to run the backtest
def run_backtest(strategy_class: TradePnlStrategy, symbol = 'IDEA.NS', from_date='2020-03-01', to_date='2022-12-30') -> Tuple[Backtest, dict]:
    current_user = get_jwt_identity()

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(50000)

    # Change according to data
    df = get_ohlc_data(symbol, from_date,to_date)
    # Convert the DataFrame to a backtrader data feed
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    backtest = Backtest.create(
        strategy=strategy_class.__name__,
        symbol=symbol,
        from_date=from_date,
        to_date=to_date,
        user_id=current_user
    )

    cerebro.addstrategy(strategy_class, {
        'backtest_obj': backtest
    })

    stats = cerebro.run()

    statistics = get_stats(cerebro, stats)
    Analysis.create(backtest_id = backtest.id, result = statistics)

    return backtest, statistics

def get_stats(cerebro: bt.Cerebro, stats: List[TradePnlStrategy]):
    strat = stats[0]

    # Gather results
    final_value = cerebro.broker.getvalue()


    if hasattr(strat, 'get_trade_statistics'):
        return strat.get_trade_statistics()
    else:
        logging.warn("Strategy without trades found")
        return None


if __name__ == '__main__':

    # Adjust the working directory and sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)

    strategies_directory = 'strategies'
    strategy_files = list_strategy_files(strategies_directory)
    
    if not strategy_files:
        print("No strategy files found.")
        sys.exit(-1)

    strategy_names = [os.path.splitext(os.path.basename(file))[0] for file in strategy_files]
    strategy_file = display_menu(strategy_files)
    strategy_name = os.path.splitext(os.path.basename(strategy_file))[0]
    
    # Add the strategies directory to the Python path
    sys.path.append(os.path.dirname(strategy_file))
    
    # Import and get the strategy class
    strategy_class = get_strategy_class(strategy_name)
    
    if not strategy_class:
        print(f"No strategy class found in {strategy_file}")
        sys.exit(-1)

    backtest, stats = run_backtest(strategy_class)
    # cerebro.plot()

