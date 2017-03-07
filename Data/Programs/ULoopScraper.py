import requests
from bs4 import BeautifulSoup as Soup

ULOOP_URL = 'http://gatech.uloop.com/housing/?rent_min=%d&rent_max=%d&beds=0&page=%d'
OUTPUT_HTML = '../Database/listings.txt'
URL_LINKS = '../Database/test.txt'
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
	for i in range(1, 15):
		html += getPage(url % (min_rent, max_rent, i))

def openFile():
	return Soup(html, 'html.parser')

def findIndividualPages():
	savePage(ULOOP_URL)
	with open(OUTPUT_HTML, 'w') as f:
		for link in openFile().find_all('a', {'class': 'title'}):
			f.write(link.get('href') + '\n')

findIndividualPages()