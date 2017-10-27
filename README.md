# EbayWebScraper
This is a personal project to gather data from specific search results for shoes sold on Ebay.

## Pre-requirements:
* Python 3
* SQLite3
* Python Requests
* BeautifulSoup4

## To Use:
1. Download dependencies with `pip install -r requirements.txt`

2. In terminal, navigate into the directory with these files.

3. Run `python shoeScraper.py` then enter your shoe search when prompted.

4. Every new search will create or update the table with the sale items' unique identifier, listing name, shoe size, date sold, and price. This will all be done in a file called "shoes_on_ebay.db".
* Data will be returned for all sold listings for shoes of US sizes 5 to 14.5 in new condition with shoe box.
