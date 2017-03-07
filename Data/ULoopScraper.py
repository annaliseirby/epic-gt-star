import requests
from bs4 import BeautifulSoup as Soup

ULOOP_URL = 'http://gatech.uloop.com/housing/?rent_min=%d&rent_max=%d&beds=0&page=%d'
SAVED_HTML = 'savedPages.txt'
OUTPUT_HTML = 'listings.txt'
URL_LINKS = 'test.txt'
min_rent = 0
max_rent = 500

def getPage(url):
	res = requests.get(url)
	if not res.ok:
		print('Could not download selected page!')
		return ''
	return res.text

def savePage(url, filename):
	html = ''
	for i in range(1, 15):
		html += getPage(url % (min_rent, max_rent, i))
	with open(filename, 'w') as f:
		f.write(Soup(html, 'html.parser').prettify())

def openFile(filename):
	with open(filename) as f:
		html = f.read()
	return Soup(html, 'html.parser')

def writeRaw():
	savePage(ULOOP_URL, SAVED_HTML)
	with open(OUTPUT_HTML, 'w') as f:
		listings = openFile(SAVED_HTML).find_all('div', {'class': 'post ad pt_1 pch_3 psub_0 nowrap pc_3'})
		for listing in listings:
			f.write(str(listing) + '\n\n')

def findIndividualPages():
	listings = str(openFile(SAVED_HTML).find_all('div', {'class': 'post ad pt_1 pch_3 psub_0 nowrap pc_3'}))
	with open(URL_LINKS, 'w') as f:
		for listing in listings:
			f.write(str(Soup(listing, 'html.parser').find('meta', {'itemprop': 'url'}).get('content')))

writeRaw()
findIndividualPages()