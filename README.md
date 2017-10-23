# EbayWebScraper
This is a personal project to gather data from specific search results for shoes sold on Ebay.

## Pre-requirements:
* Python 3
* Python Requests
* BeautifulSoup4
* SQLite3

## To Use:
1. Download dependencies.

2. In terminal, navigate into the directory with these files.

3. Run `python shoeScraper.py` then enter your shoe search when prompted.

4. Every new search will create or update the table with the sale items' unique identifier, listing name, shoe size, date sold, and price. This will all be done in a file called "shoes_on_ebay.db".
⋅⋅* Data will be returned for all sold listings for shoes of US sizes 5 to 14.5 in new condition with shoe box.
⋅⋅* `shoes_on_ebay.db` can serve as an example file or base data. You may delete this. If deleted, first run of `shoeScraper.py` will create a new `shoes_on_ebay.db` file. If not, the file will be added to.
