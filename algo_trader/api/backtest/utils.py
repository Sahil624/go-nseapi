import os
import importlib
import inspect

from strategies.base_strategy.base import TradePnlStrategy


def list_strategy_files(strategies_directory = 'strategies'):
    strategy_files = []
    for root, _, files in os.walk(strategies_directory):
        for file in files:
            if file.endswith("_stg.py"):  # Identifies strategy files
                strategy_files.append(os.path.join(root, file))
    return strategy_files

def get_strategy_names(strategy_files):
    strategy_names = [os.path.splitext(os.path.basename(file))[0] for file in strategy_files]
    return strategy_names

def load_strategy_class(strategy_name: str):
    stg_module = strategy_name.replace("_stg", "")
    module_name = f"strategies.{stg_module}.{strategy_name}"
    try:
        strategy_module = importlib.import_module(module_name)
        strategy_classes = inspect.getmembers(strategy_module, inspect.isclass)
        for name, cls in strategy_classes:
            if issubclass(cls, TradePnlStrategy) and cls is not TradePnlStrategy:
                return cls
        print(f"No suitable strategy class found in {module_name}")
        return None
    except (ImportError, AttributeError) as e:
        print(f"Error importing strategy: {e}")
        return None