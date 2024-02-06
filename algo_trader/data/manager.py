import logging
import pandas as pd
from .nse_downloader import download_and_save_ohlc
import os

def get_ohlc_data(symbol, from_date, to_date, output_folder="ohlc_csv") -> pd.DataFrame:
    csv_path = os.path.join(output_folder, f'{symbol}-EQ.csv')
    
    # Convert from_date and to_date to Timestamp for comparison
    from_date = pd.Timestamp(from_date)
    to_date = pd.Timestamp(to_date)

    # Try to load existing data
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
        mask = (existing_df.index >= from_date) & (existing_df.index <= to_date)
        filtered_df = existing_df.loc[mask]

        # Check if the data is complete
        if not filtered_df.empty and filtered_df.index.min() <= from_date and filtered_df.index.max() >= to_date:
            print("All data found in cache.")
            return filtered_df
        else:
            print(f"Downloading delta ||  Min present {filtered_df.index.min()}. (Requested From {from_date}) || Max Present {filtered_df.index.max()} (Requested To {to_date})")
            # Download missing data
            download_and_save_ohlc(symbol, from_date, to_date, output_folder)
            existing_df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
            mask = (existing_df.index >= from_date) & (existing_df.index <= to_date)
            filtered_df = existing_df.loc[mask]
            return filtered_df
    else:
        print("Downloading whole data")
        # If no existing file, download data
        download_and_save_ohlc(symbol, from_date, to_date, output_folder)
        existing_df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
        mask = (existing_df.index >= from_date) & (existing_df.index <= to_date)
        filtered_df = existing_df.loc[mask]
        return filtered_df
