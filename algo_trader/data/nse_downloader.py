import argparse
from datetime import datetime
import yfinance as yf
import pandas as pd
import os

def download_and_save_ohlc(symbol, from_date, to_date, output_folder):
    print(f"Downloading data for {symbol} from {from_date} to {to_date}")
    # Download stock data using yfinance
    new_df = yf.download(symbol, start=from_date, end=to_date, progress=False)
    
    # Add 'Date' column from the index
    new_df['Date'] = new_df.index

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Path for the CSV file
    csv_path = os.path.join(output_folder, f'{symbol}-EQ.csv')

    # If the file exists, load existing data
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path, parse_dates=['Date'])
        
        # Combine the new data with the existing data, dropping duplicates
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['Date']).sort_values(by='Date')
    else:
        combined_df = new_df

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(csv_path, index=False)

    print(f'Saved OHLC data to {csv_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and save OHLC data for a given symbol and date range.')
    parser.add_argument('--symbol', type=str, required=True, help='Stock symbol (e.g., SBIN)')
    parser.add_argument('--from_date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').strftime('%Y-%m-%d'), required=True, help='From date (YYYY-MM-DD)')
    parser.add_argument('--to_date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').strftime('%Y-%m-%d'), required=True, help='To date (YYYY-MM-DD)')
    parser.add_argument('--output_folder', type=str, default='ohlc_csv', help='Output folder for saving the CSV files')

    args = parser.parse_args()

    download_and_save_ohlc(args.symbol, args.from_date, args.to_date, args.output_folder)
