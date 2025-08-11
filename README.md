# Max Pain Scraper

This Python script scrapes the "Max Pain" price for a given stock ticker and options expiration date from the website [optioncharts.io](https://optioncharts.io).

## Description

The script calculates the Max Pain price, which is the strike price with the most open interest for options (puts and calls), representing the price at which the maximum number of options holders would lose money on their investment. This script is pre-configured to fetch the Max Pain prices for the "Magnificent Seven" stocks.

## How it Works

The script performs the following steps:

1.  **Constructs a URL**: For each stock ticker, it creates a unique URL for `optioncharts.io` that specifies the ticker and the desired options expiration date.
2.  **Fetches HTML**: It sends an HTTP GET request to the constructed URL and retrieves the raw HTML content of the webpage.
3.  **Parses HTML**: Using the BeautifulSoup library, the script parses the HTML to navigate its structure.
4.  **Extracts Price**: It locates the specific HTML paragraph tag (`<p>`) that contains the Max Pain price and then extracts the price value from a bold tag (`<b>`) within that paragraph.
5.  **Iterates and Prints**: The main part of the script iterates through a predefined list of stock tickers, calls the scraping function for each one, and prints the result to the console.

## Dependencies

The script requires the following Python libraries:

- `requests`
- `beautifulsoup4`

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, simply execute it from your terminal:

```bash
python max_pain_scraper.py
```

The script is currently hardcoded to fetch the Max Pain prices for the following tickers: `AAPL`, `AMZN`, `GOOG`, `GOOGL`, `META`, `MSFT`, `NVDA`, and `TSLA` with an expiration date of `2025-08-15`. You can modify the `magnificent_seven` list and the `expiration_date` variable in the script to fetch data for other tickers and dates.

## Example Output

```
Fetching Max Pain prices for options expiring on 2025-08-15
------------------------------
AAPL: $175.00
AMZN: $130.00
GOOG: $140.00
GOOGL: $140.00
META: $280.00
MSFT: $350.00
NVDA: $450.00
TSLA: $250.00
```

*(Note: The prices above are examples and will vary.)*

## Disclaimer

This script is for educational purposes only. The data provided is scraped from a third-party website and may not be accurate. It is not financial advice. Please do your own research before making any investment decisions.
