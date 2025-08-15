#!/Users/okato/miniconda3/envs/work/bin/python
import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import configparser

HISTORY_FILE = 'max_pain_history.json'

def get_max_pain(ticker, expiration_date):
    url = f"https://optioncharts.io/async/options_charts/max_pain?expiration_dates={expiration_date}%3Am&option_type=all&strike_range=all&ticker={ticker}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        p_tag = soup.find('p', class_='tw-mb-3 tw-text-gray-700 tw-text-sm')
        if p_tag:
            price_tag = p_tag.find_all('b')[-1]
            if price_tag:
                return price_tag.text.strip()
        
        return "Max Pain price not found."
            
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"

def load_previous_results():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_results(results):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('watchlist.ini')
    stocks_str = config.get('watchlist', 'stocks', fallback='AAPL, AMZN, GOOG, GOOGL, META, MSFT, NVDA, TSLA')
    watchlist = [stock.strip() for stock in stocks_str.split(',')]
    
    # We can either calculate the next Friday or hardcode it if we know it.
    # For this week, Friday is August 15, 2025
    expiration_date = "2025-08-15" #get_next_friday()
    
    previous_results = load_previous_results()
    current_results = {}

    print(f"Fetching Max Pain prices for options expiring on {expiration_date}")
    print("-" * 30)
    
    for ticker in watchlist:
        max_pain_price_str = get_max_pain(ticker, expiration_date)
        print(f"{ticker}: {max_pain_price_str}")
        
        if max_pain_price_str and "Error" not in max_pain_price_str and "not found" not in max_pain_price_str:
            try:
                # Clean the string and convert to float
                current_price = float(max_pain_price_str.replace('$', '').replace(',', ''))
                current_results[ticker] = current_price
                
                if ticker in previous_results:
                    previous_price = previous_results[ticker]
                    difference = current_price - previous_price
                    print(f"  - Previous: ${previous_price:,.2f}, Change: ${difference:,.2f}")
            except ValueError:
                print(f"  - Could not parse price for {ticker}")


    if current_results:
        save_results(current_results)