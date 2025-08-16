#!/Users/okato/miniconda3/envs/work/bin/python
import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import configparser
import finnhub

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

def get_current_price(ticker, finnhub_client):
    try:
        quote = finnhub_client.quote(ticker)
        return quote['c']
    except Exception as e:
        return f"Error fetching current price for {ticker}: {e}"

def load_previous_results():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_results(results):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(results, f, indent=4)

def get_next_friday():
    today = datetime.date.today()
    days_until_friday = (4 - today.weekday() + 7) % 7
    next_friday = today + datetime.timedelta(days=days_until_friday)
    return next_friday.strftime("%Y-%m-%d")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    stocks_str = config.get('watchlist', 'stocks', fallback='AAPL, AMZN, GOOG, GOOGL, META, MSFT, NVDA, TSLA')
    watchlist = [stock.strip() for stock in stocks_str.split(',')]

    finnhub_api_key = os.environ.get('API_KEY') or config.get('finnhub', 'api_key', fallback=None)
    if not finnhub_api_key:
        print("Finnhub API key not found. Please set the API_KEY environment variable or add it to config.ini under the [finnhub] section.")
        exit()

    finnhub_client = finnhub.Client(api_key=finnhub_api_key)

    expiration_date = get_next_friday()
    
    previous_results = load_previous_results()
    current_results = {}

    print(f"Fetching Max Pain prices for options expiring on {expiration_date}")
    print("-" * 30)
    
    for ticker in watchlist:
        max_pain_price_str = get_max_pain(ticker, expiration_date)
        current_price = get_current_price(ticker, finnhub_client)
        
        print(f"{ticker}:")
        print(f"  - Max Pain: {max_pain_price_str}")

        max_pain_price = None
        if max_pain_price_str and "Error" not in max_pain_price_str and "not found" not in max_pain_price_str:
            try:
                max_pain_price = float(max_pain_price_str.replace('$', '').replace(',', ''))
            except ValueError:
                print(f"  - Could not parse max pain price for {ticker}")

        if isinstance(current_price, float):
            if max_pain_price is not None:
                price_difference = current_price - max_pain_price
                print(f"  - Current Price: ${current_price:,.2f} (${price_difference:,.2f})")
            else:
                print(f"  - Current Price: ${current_price:,.2f}")
        else:
            print(f"  - Current Price: {current_price}")

        if max_pain_price is not None:
            current_results[ticker] = max_pain_price
            if ticker in previous_results:
                previous_price = previous_results[ticker]
                difference = max_pain_price - previous_price
                print(f"  - Previous Max Pain: ${previous_price:,.2f}, Change: ${difference:,.2f}")

    if current_results:
        save_results(current_results)
