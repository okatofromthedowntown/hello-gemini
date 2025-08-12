#!/Users/okato/miniconda3/envs/work/bin/python
import requests
from bs4 import BeautifulSoup
import datetime

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

if __name__ == "__main__":
    magnificent_seven = ["AAPL", "AMZN", "GOOG", "GOOGL", "META", "MSFT", "NVDA", "TSLA"]
    
    # We can either calculate the next Friday or hardcode it if we know it.
    # For this week, Friday is August 15, 2025
    expiration_date = "2025-08-15" #get_next_friday()
    
    print(f"Fetching Max Pain prices for options expiring on {expiration_date}")
    print("-" * 30)
    
    for ticker in magnificent_seven:
        max_pain_price = get_max_pain(ticker, expiration_date)
        print(f"{ticker}: {max_pain_price}")

