import requests
import json
from bs4 import BeautifulSoup as Soup
from geopy.geocoders import Nominatim

ULOOP_URL = 'http://gatech.uloop.com/housing/?rent_min=%d&rent_max=%s&beds=0&page=%d'
OUTPUT_HTML = '../Database/listings.json'
min_rent = 10
max_rent = ''


# Returns the raw html of each page
def getPage(url):
    res = requests.get(url)
    if not res.ok:
        print('Could not download selected page!')
        return ''
    return res.text


# Finds all of the links on all of the pages
# The next step is to eliminate redundancy in the links
def findAllLinks(url):
    links = set()
    # for i in range(1, findNumPages()):
    for i in range(1, 3):
        print(i)
        html = getPage(url % (min_rent, max_rent, i))
        links.update(findIndividualPages(html))
    return links

# Returns a new Beautiful soup object
def openFile(html):
    return Soup(html, 'html.parser')


# Finds the number of pages that needs to be returned and returns it
def findNumPages():
    html = getPage(ULOOP_URL % (min_rent, max_rent, 1))
    # This string contains the total number of listings and the number of listings per page
    numToBeParsed = openFile(html).find('p', {'class': 'listing_founded'}).get_text().split()
    numListings = int(numToBeParsed[1])
    numOnPage = int(numToBeParsed[4].split('-')[1])
    # Sorry for the ternary here, it's just to get rid of the truncation that python does
    return numListings // numOnPage + 2 if numListings % numOnPage != 0 else 1


# Finds the individual links for each web page
def findIndividualPages(html):
    links = set()
    for link in openFile(html).find_all('a', {'class': 'title'}):
        links.add(link.get('href'))
    return links


# Extracts information from each web page
def dataFromPage():
    with open(OUTPUT_HTML, 'w') as f:
        f.write('list = [\n')
        for link in findAllLinks(ULOOP_URL):
            try:
                data = []
                html = Soup(getPage(link), 'html.parser')
                data.append(html.find('h1', {'class': 'listing_title'}).get_text())
                information = html.find_all('div', {'class': 'table_td'})
                for i in range(1, 4):
                    data.append('null')
                data.append(link)
                for info in information:
                    if data[1] == 'null' and ', Atlanta, GA' in info.get_text():
                        latLong = turnAddressToGeocode(info.get_text())
                        data[1] = latLong[0]
                        data[2] = latLong[1]
                    elif data[3] == 'null' and '$' in info.get_text():
                        data[3] = info.get_text()[1:]
                    if data[1] != 'null' and data[3] != 'null':
                        print('One down!')
                        break
                if data[1] != 'null':
                    # This information is useless if we don't have the address
                    writeToFile(data, f)
            except AttributeError:
                # Uloop doesn't always update all of their listings, so we have to catch this here
                print()
        f.write(']')
        print("I'm done!")


# Writes all the given data to the file
def writeToFile(data, f):
    format = ('{\n\tname: "%s", \n\tgeocode: {\n\t\tlat: %f, \n\t\tlng: %f \n\t}, \n\tprice: %s, \n\tlink: "%s"\n},')
    # format = '\t{"listing": {"title": "%s", "address": "%s", "rent": "%s", "link": "%s"}}, \n'
    f.write(format % tuple(data))


# Turns the raw address into a usable array of latitude and longitude
def turnAddressToGeocode(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    return [location.latitude, location.longitude]


dataFromPage()
