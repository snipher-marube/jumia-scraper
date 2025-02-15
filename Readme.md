# Jumia Product Scraper

This project is a web scraper for Jumia, an online shopping website. The scraper is built using Playwright and Python, and it allows you to scrape product information based on a search query.

## Features

- Scrapes product information from Jumia
- Extracts product title, price, discount, link, and image
- Supports saving the scraped data in CSV or JSON format
- Configurable number of pages to scrape

## Requirements

- Python 3.7+
- Playwright

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/snipher-marube/jumia-scraper.git
    cd jumia-scraper
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .env
    source .env/bin/activate  # On Windows use `.env\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    playwright install
    ```

## Usage

To run the scraper, use the following command:
```sh
python scrapper.py