#imports
import sqlite3
import re
import requests

from bs4 import BeautifulSoup as soup

#DECLARE SQL:
conn = sqlite3.connect('chucksOnEbay.db')
c = conn.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS chucks (id TEXT, list_title TEXT, shoe_size REAL, date_sold TEXT, price REAL)")

def data_entry():
	c.execute("INSERT INTO chucks (id, list_title, shoe_size, date_sold, price) VALUES (?, ?, ?, ?, ?)",
		(item_id, item_title, shoe_size, item_date, item_price))
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

#sizes = ['5','5%252E5','6','6%252E5','7','7%252E5','8','8%252E5','9','9%252E5','10','10%252E5','11','11%252E5','12','12%252E5','13','13%252E5','14','14%252E5']
shoe_size = 5.0

while shoe_size < 15.0:

	my_url = 'https://www.ebay.com/sch/i.html'

	params = {
		'_from' : 'R40',
		'_sacat' : 0,
		'LH_Complete' : 1,
		'LH_Sold' : 1,
		'LH_ItemCondition' : 1000,
		'_nkw' : 'converse chuck taylor 2',
		'_dcat' : 15709,
		"US%20Shoe%20Size%20%28Men%27s%29" : shoe_size,
		'rt' : 'nc',
	}
	r = requests.get(my_url, params=params)

	# html parsing
	page_soup = soup(r.text, "html.parser")

	#class nllclt is only there when there are 0 results
	if bool(page_soup.find("span", {"class": "nllclt"})) == True:
		continue

	#find the first of this only because Ebay sometimes adds suggested results that don't match right away
	matches = page_soup.find("ul", class_= "gv-ic")

	# grabs each sale
	containers = matches.findAll("li",{"class":"sresult"})

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


		float(shoe_size)

		#write outputs in csv file and format accordingly
		data_entry()

		shoe_size += 0.5

# always close db connection when done writing it
c.close()
conn.close()

#print output in terminal to know that it went all the way through
print("check the database!")

