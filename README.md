# Max Pain Scraper

This Python script scrapes the "Max Pain" price for a given stock ticker and options expiration date from the website [optioncharts.io](https://optioncharts.io). It also fetches the current stock price from Finnhub and compares it to the Max Pain price.

## Description

The script calculates the Max Pain price, which is the strike price with the most open interest for options (puts and calls), representing the price at which the maximum number of options holders would lose money on their investment. The script is configurable to any stock ticker.

## How it Works

The script performs the following steps:

1.  **Reads Configuration**: It reads the `config.ini` file to get the watchlist of stocks and the Finnhub API key.
2.  **Constructs a URL**: For each stock ticker, it creates a unique URL for `optioncharts.io` that specifies the ticker and the desired options expiration date.
3.  **Fetches HTML**: It sends an HTTP GET request to the constructed URL and retrieves the raw HTML content of the webpage.
4.  **Parses HTML**: Using the BeautifulSoup library, the script parses the HTML to navigate its structure.
5.  **Extracts Price**: It locates the specific HTML paragraph tag (`<p>`) that contains the Max Pain price and then extracts the price value from a bold tag (`<b>`) within that paragraph.
6.  **Fetches Current Price**: It uses the Finnhub API to get the current price of the stock.
7.  **Compares Prices**: It calculates the difference between the current price and the Max Pain price.
8.  **Loads History**: It loads the previous Max Pain prices from `max_pain_history.json`.
9.  **Compares History**: It compares the current Max Pain price with the previous price and shows the change.
10. **Saves History**: It saves the current Max Pain prices to `max_pain_history.json` for future comparisons.
11. **Iterates and Prints**: The main part of the script iterates through the watchlist, calls the scraping and fetching functions for each one, and prints the result to the console.

## Dependencies

The script requires the following Python libraries:

- `requests`
- `beautifulsoup4`
- `finnhub-python`

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```

## Configuration

1.  **Create `config.ini`**:
    Create a `config.ini` file in the same directory as the script. You can copy the `config.ini.example` file and rename it to `config.ini`.

2.  **Set Watchlist**:
    In the `config.ini` file, under the `[watchlist]` section, add the stock tickers you want to track, separated by commas.

    ```ini
    [watchlist]
    stocks = AAPL, AMZN, GOOG, GOOGL, META, MSFT, NVDA, TSLA
    ```

3.  **Set Finnhub API Key**:
    You need a Finnhub API key to fetch the current stock prices. You can get a free API key from [finnhub.io](https://finnhub.io).

    You can set the API key in one of two ways:

    -   **Environment Variable (Recommended)**:
        Set the `API_KEY` environment variable to your Finnhub API key.

        ```bash
        export API_KEY=YOUR_API_KEY
        ```

    -   **`config.ini` file**:
        In the `config.ini` file, under the `[finnhub]` section, add your API key.

        ```ini
        [finnhub]
        api_key = YOUR_API_KEY
        ```

## Usage

To run the script, simply execute it from your terminal:

```bash
python max_pain_scraper.py
```

The script will fetch the Max Pain prices for the stocks in your watchlist and display the results in the console.

## Example Output

```
Fetching Max Pain prices for options expiring on 2025-08-15
------------------------------
AAPL:
  - Max Pain: $175.00
  - Current Price: $172.50 (-$2.50)
  - Previous Max Pain: $170.00, Change: $5.00
AMZN:
  - Max Pain: $130.00
  - Current Price: $132.80 (+$2.80)
  - Previous Max Pain: $130.00, Change: $0.00
...
```

*(Note: The prices above are examples and will vary.)*

## History

The script stores the last fetched Max Pain prices in the `max_pain_history.json` file. This allows the script to compare the current prices with the previous ones and show the changes.

## Disclaimer

This script is for educational purposes only. The data provided is scraped from a third-party website and may not be accurate. It is not financial advice. Please do your own research before making any investment decisions.