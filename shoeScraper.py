#imports
import sqlite3
import re
import requests
from bs4 import BeautifulSoup as soup

shoe_search = input('What shoe would you like to search for? ')
SQL_name = shoe_search.replace(" ", "_")

sizePrompted = input('''
	Would you like to search for a certain size?
	(enter "no" to search all sizes)
	(enter "11" to search for size 11)
	(enter "9.5 to 10.5" to search sizes 9.5, 10, and 10.5)
	''')

anyButNumbersAndPeriod = re.compile("([^0-9.])")

if (sizePrompted.lower() == "no"):
	sizeMin = 5
	sizeMax = 15

	print("searching for all sizes 5 through 14")
elif "-" in sizePrompted and not anyButNumbersAndPeriod.match(sizePrompted):
	#this is a range
	sizePrompted = sizePrompted.split("-");
	sizeMin = float(sizePrompted[0]);
	sizeMax = float(sizePrompted[1]);

	print("searching for sizes " + sizePrompted[0] + " through " + sizePrompted[1])
elif not anyButNumbersAndPeriod.match(sizePrompted):
	#single size
	sizeMin = float(sizePrompted)
	sizeMax = sizeMin

	print("searching for size " + sizePrompted)
else:
	print("Please enter a valid size\n")

#DECLARE SQL:
conn = sqlite3.connect('shoes_on_ebay.db')
c = conn.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS " + SQL_name + " (id TEXT, list_title TEXT, shoe_size REAL, date_sold TEXT, price REAL)")

def data_entry():
	c.execute("INSERT INTO " + SQL_name + " (id, list_title, shoe_size, date_sold, price) VALUES (?, ?, ?, ?, ?)",
		(item_id, item_title, shoe_size, item_date, item_price))
	conn.commit()

def no_duplicates(x):
	c.execute("SELECT id FROM " + SQL_name + " WHERE id = ?", (x,))
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


sizes = []

for size in range(5,14):
	sizes.append(str(size))
	half_size = str(size) + '%2E5'
	sizes.append(half_size)

for size in sizes:

	my_url = 'https://www.ebay.com/sch/i.html'

	params = {
		'_from' : 'R40',
		'_sacat' : 0,
		'LH_Complete' : 1,
		'LH_Sold' : 1,
		'LH_ItemCondition' : 1000,
		'_nkw' : shoe_search,
		'_dcat' : 15709,
		"US%20Shoe%20Size%20%28Men%27s%29" : size,
		'rt' : 'nc',
	}

	r = requests.get(my_url, params=params)

	# html parsing
	page_soup = soup(r.text, "html.parser")

	#class nllclt is only there when there are 0 results
	if bool(page_soup.find("span", {"class": "nllclt"})) == True:
		continue

	#find the first of this only because Ebay sometimes adds suggested results that don't match right away
	matches = page_soup.find("ul", {"class": "gv-ic"})

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

		#reformat half sizes before entering
		shoe_size = size.replace("%2E", ".")

		float(shoe_size)

		#write outputs in csv file and format accordingly
		data_entry()

# always close db connection when done writing it
c.close()
conn.close()

#print output in terminal to know that it went all the way through
print("check the database!")

