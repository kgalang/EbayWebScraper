# EbayWebScraper
This is a personal project to gather data from specific search results for Ebay sales.

To use, run with Python 3, BeautifulSoup4, and SQLite3, then type in which shoe you would like to search for. Data will be returned for all sold listings for shoes of US sizes 5 to 14.5 in new condition with shoe box.

Every new search will create or update the table with the sale items' unique identifier, listing name, shoe size, date sold, and price. This will all be done in a file called "shoes_on_ebay.db". If this file does not exist, it will be created. If it does exist, it will be updated.
