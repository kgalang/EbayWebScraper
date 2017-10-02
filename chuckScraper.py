#imports
import sqlite3
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#DECLARE ALL SQL FUNCTIONS:
conn = sqlite3.connect('chucksOnEbay.db')
c = conn.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS chucks(id TEXT, list_title TEXT, date_sold TEXT, price REAL)")

def data_entry():
	c.execute("INSERT INTO chucks (id, list_title, date_sold, price) VALUES (?, ?, ?, ?)",
		(item_id, item_title, item_date, item_price))
	conn.commit()

def no_duplicates(x):
	c.execute("SELECT id FROM chucks WHERE id = ?", (x,))
	data = c.fetchone()
	if data is None:
		return 0
	else:
		return 1

def date_format(date):
	months = {"Jan" : '01', "Feb" : '02', "Mar" : '03', "Apr" : '04', "May" : '05', "Jun" : '06', "Jul" : '07', "Aug" : '08', "Sep" : '09', "Oct" : '10', "Nov" : '11', "Dec" : '12'}
	month = str(date[:3])
	day = str(date[4:6])
	month_num = months[month]
	return month_num + "/" + day

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
containers = page_soup.findAll("li",{"class":"sresult"})

# Create table, comment out after making it the first time
create_table()

for container in containers:
	#extract unique identifier
	#all ints in python 3 are long longs
	item_id = container.get("id")

	#if item_id exists, loop to next entry
	if no_duplicates(item_id) == 1:
		continue

	# extract item title from html
	item_title = container.h3.a.text
	
	# extract date and time sold from html
	date_container = container.find("span", {"class":"lcol"})
	date = date_container.text[:6]
	item_date = date_format(date).strip()

	# extract price
	price_container = container.find("span", {"class":"bidsold"}) 
	# strip data to clean up and fix formatting
	item_price = price_container.text.replace("$", "").strip()
	#if has "\xa0to " get the average
	if bool(re.search("\xa0to ", item_price)) == False:
		item_price = item_price
	elif bool(re.search("\xa0to ", item_price)) == True:
		arr = item_price.split("\xa0to ")
		p1 = float(arr[0])
		p2 = float(arr[1])
		item_price = (p1 + p2) / 2.00

	#write outputs in csv file and format accordingly
	data_entry()

# always close csv file when done writing it
c.close()
conn.close()

#print output in terminal to know that it went all the way through
print("check the database!")

