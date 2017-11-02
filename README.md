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

3. Run `python shoeScraper.py` then enter your shoe search and size when prompted.

4. The average selling price for your shoes for the specified sizes will be displayed.

5. Every search will create or update the table with the sale items' unique identifier, listing name, shoe size, date sold, and price. This will all be done in a file called "shoes_on_ebay.db".
  * Data will be returned for all sold listings for shoes new condition with shoe box with the searched size.
