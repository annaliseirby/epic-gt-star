import requests
import json
from bs4 import BeautifulSoup as Soup

ULOOP_URL = 'http://gatech.uloop.com/housing/?rent_min=%d&rent_max=%d&beds=0&page=%d'
OUTPUT_HTML = '../Database/listings.json'
html = ''
min_rent = 0
max_rent = 500

# Returns the html of each page
def getPage(url):
	res = requests.get(url)
	if not res.ok:
		print('Could not download selected page!')
		return ''
	return res.text

# Saves the html of each page in a global string
# There's probably a better way of doing this, so if you're reading this, sorry
def savePage(url):
	global html
	for i in range(1, 16):
		html += getPage(url % (min_rent, max_rent, i))

def openFile():
	return Soup(html, 'html.parser')

# Finds the individual links for each web page
def findIndividualPages():
	savePage(ULOOP_URL)
	links = []
	for link in openFile().find_all('a', {'class': 'title'}):
		links.append(link.get('href'))
	return links

# Extracts information from each web page
def dataFromPage():
	with open(OUTPUT_HTML, 'w') as f:
		f.write('[')
		for link in findIndividualPages():
			data = []
			html = Soup(getPage(link), 'html.parser')
			data.append(html.find('h1', {'class': 'listing_title'}).get_text());
			information = html.find_all('div', {'class': 'table_td'})
			for i in range(5, 10):
				data.append(information[i].get_text())
			f.write('{"listing": {"title": "%s", "address": "%s", "distanceToCampus": "%s", "bedroom": "%s", "bathroom": "%s", "rent": "%s"}}, \n' % tuple(data))
		f.write(']')
		print("I'm done!")

dataFromPage()