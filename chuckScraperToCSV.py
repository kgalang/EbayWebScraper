#Get data from ebay search link and find average price for shoes

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_dcat=15709&US%2520Shoe%2520Size%2520%2528Men%2527s%2529=8%7C8%252E5%7C9%7C9%252E5%7C10%7C10%252E5%7C11%7C11%252E5%7C12%7C13&Product%2520Line=Chuck%2520Taylor%2520All%2520Star&Brand=Chuck%2520Taylor%7CConverse&LH_ItemCondition=1000&LH_Complete=1&LH_Sold=1&_nkw=converse+chuck+taylor+2&rt=nc&LH_BIN=1'

#Opening connection and grabbing the page
uClient = uReq(my_url)
#make var before .read() so you don't lose the data
page_html = uClient.read()
#close the client because it is an open connection
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each sale
containers = page_soup.findAll("div",{"class":"itmcd"})

filename = "ebay_sales.csv"
f = open(filename, "w")

headers = "Title, Date, Time, Price\n"

f.write(headers)

for container in containers:
	# extract item title from html
	item_title = container.h3.a.text
	
	# extract date and time sold from html
	date_container = container.find("span", {"class":"lcol"})
	item_date = date_container.text

	# extract price
	price_container = container.find("span", {"class":"bidsold"}) 
	# strip data to clean up and fix formatting in csv
	item_price = price_container.text.strip()

	#print output in terminal
	print("Item Title: " + item_title)
	print("Item Date: " + item_date)
	print("Item Price: " + item_price)

	#write outputs in csv file and format accordingly
	f.write(item_title.replace(",", "|") + "," + item_date.replace(" ", ",") + "," + item_price + "\n")
# always close csv file when done writing it
f.close()