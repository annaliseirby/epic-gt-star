import requests
import json
from bs4 import BeautifulSoup as Soup

ULOOP_URL = 'http://gatech.uloop.com/housing/?rent_min=%d&rent_max=%s&beds=0&page=%d'
OUTPUT_HTML = '../Database/listings.json'
html = ''
min_rent = 0
max_rent = ''

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
	for i in range(1, findNumPages() + 1):
		html += getPage(url % (min_rent, max_rent, i))
		print(i)

def openFile():
	return Soup(html, 'html.parser')

def findNumPages():
	global html
	html = getPage(ULOOP_URL % (min_rent, max_rent, 1))
	numListings = int(openFile().find('p', {'class':'listing_founded'}).get_text().split()[1])
	numOnPage = int(openFile().find('p', {'class':'listing_founded'}).get_text().split()[4].split('-')[1])
	return numListings // numOnPage + 1 if numListings % numOnPage != 0 else 0

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
		f.write('[\n')
		for link in findIndividualPages():
			try:
				data = []
				html = Soup(getPage(link), 'html.parser')
				data.append(html.find('h1', {'class': 'listing_title'}).get_text());
				information = html.find_all('div', {'class': 'table_td'})
				for i in range(1, 4):
					data.append('null')
				for info in information:
					if data[1] == 'null' and ' , Atlanta, GA' in info.get_text():
						data[1] = info.get_text()
					elif data[2] == 'null' and ' miles' in info.get_text():
						data[2] = info.get_text()
					elif data[3] == 'null' and '$' in info.get_text():
						data[3] = info.get_text()
					if data[1] != 'null' and data[2] != 'null' and data[3] != 'null':
						break
				f.write('\t{"listing": {"title": "%s", "address": "%s", "distanceToCampus": "%s", "rent": "%s"}}, \n' % tuple(data))
			except AttributeError:
				f.write(']')
		f.write(']')
		print("I'm done!")

dataFromPage()