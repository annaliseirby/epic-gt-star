import requests
from bs4 import BeautifulSoup as Soup
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

MAIN_URL = 'https://www.homeparkrentals.com/listings/'
OUTPUT_FILE = '../Database/listings2.json'


# Returns the raw html of each page
def getPage(url):
    res = requests.get(url)
    if not res.ok:
        print('Could not download selected page!')
        return ''
    return res.text


# Returns a new Beautiful soup object
def openFile(url):
    return Soup(getPage(url), 'html.parser')


# Finds the individual links
def findIndividualPages(url):
    links = []
    for link in openFile(url).find_all('li', {'class': 'property_title'}):
        links.append(link.find('a').get('href'))
    return links


# Gets the data from each page
def dataFromPage():
    f = open(OUTPUT_FILE, 'w')
    f.write('[')
    allHomes = []
    for link in findIndividualPages(MAIN_URL):
        html = openFile(link)
        data = []
        data.append(html.find('h1', {'class': 'property-title'}).get_text())
        temp = html.find('li', {'class': 'property_location'}).find('span', {'class': 'value'}).get_text()
        temp = cleanUpData(temp)
        data.append(temp)
        geoData = turnAddressToGeocode(temp)
        data.extend(geoData)
        temp = html.find('li', {'class': 'property_price'}).find('span', {'class': 'value'}).get_text()
        data.append(cleanUpData(temp))
        data.append(link)
        writeToFile(data, f)
        allHomes.append(data)
    f.write(']')
    f.close()


# Removes dollar signs, escape characters and commas from data
def cleanUpData(data):
    data = data.strip('\xa0')
    if '$' in data:
        data = data.split('$')[1].replace(',', '')
    else:
        data = ' '.join(data.split())
    return data


# Turns the raw address into a usable array of latitude and longitude
def turnAddressToGeocode(address):
    geolocator = Nominatim()
    try:
        location = geolocator.geocode(address)
        return [location.latitude, location.longitude]
    # If the geocoder times out, or if the geocoder returns null, we catch it
    except (GeocoderTimedOut, AttributeError):
        return ['null', 'null']


# Writes all the given data to the file
def writeToFile(data, f):
    format = '{\n\t"name": "%s", \n\t"geocode": {\n\t\t"address": "%s", \n\t\t"lat": %s, \n\t\t"lng": %s \n\t}, \n\t"price": %s, \n\t"link": "%s"\n},'
    f.write(format % tuple(data))


dataFromPage()
