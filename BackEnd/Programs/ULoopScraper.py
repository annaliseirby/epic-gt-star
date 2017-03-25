import requests
from bs4 import BeautifulSoup as Soup
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

ULOOP_URL = 'http://gatech.uloop.com/housing/?rent_min=%d&rent_max=%s&beds=0&page=%d'
OUTPUT_FILE = '../Database/listings.json'
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
def findAllLinks(url):
    links = set()
    for i in range(1, findNumPages()):
        html = getPage(url % (min_rent, max_rent, i))
        links.update(findIndividualPages(html))
    return links


# Returns a new Beautiful soup object
def openFile(html):
    return Soup(html, 'html.parser')


# Finds the number of pages that needs to be returned and returns it
def findNumPages():
    html = getPage(ULOOP_URL % (min_rent, max_rent, 1))
    # This string contains the total number of listings and the number of
    # listings per page
    # It looks like this: "Found 298 listings, displaying 1-20"
    numToBeParsed = openFile(html).find('p',
            {'class': 'listing_founded'}).get_text().split()
    numListings = int(numToBeParsed[1])
    numOnPage = int(numToBeParsed[4].split('-')[1])
    numPages = numListings // numOnPage
    # If there's any extra, there's an extra page
    if numListings % numOnPage != 0:
        numPages += 1
    return numPages + 1


# Finds the individual links for each web page
def findIndividualPages(html):
    links = set()
    for link in openFile(html).find_all('a', {'class': 'title'}):
        links.add(link.get('href'))
    return links


# Extracts information from each web page
# The array will be of the format title, geocode (either address or latLong)
# then price and link
# Eventually need to move logic from here to helper methods
def dataFromPage():
    f = open(OUTPUT_FILE, 'w')
    f.write('[\n')
    for link in findAllLinks(ULOOP_URL):
        try:
            data = []
            html = openFile(getPage(link))
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
                # If both parts of the array are not null, we're done!
                if data[1] != 'null' and data[3] != 'null':
                    break
            # This information is useless if we don't have the address
            if data[1] != 'null':
                if data[2] == 'null':
                    writeToFile(data, f, False)
                else:
                    writeToFile(data, f, True)
        except AttributeError:
            print()
    f.write(']')
    f.close()
    print("I'm done!")


# Turns the raw address into a usable array of latitude and longitude
def turnAddressToGeocode(address):
    geolocator = Nominatim()
    try:
        location = geolocator.geocode(address)
        return [location.latitude, location.longitude]
    # If the geocoder times out, or if the geocoder returns null, we catch it
    except (GeocoderTimedOut, AttributeError):
        return [address, 'null']


# Writes all the given data to the file
# The second boolean is in case geopy is unable to fully parse the address
def writeToFile(data, f, fullyParsed):
    if fullyParsed:
        format = '{\n\t"name": "%s", \n\t"geocode": {\n\t\t"lat": %f, \n\t\t"lng": %f \n\t}, \n\t"price": %s, \n\t"link": "%s"\n},'
    else:
        data = [data[0], data[1], data[3], data[4]]
        format = '{\n\t"name": "%s", \n\t"geocode": {\n\t\t"address": "%s" \n\t}, \n\t"price": %s, \n\t"link": "%s"\n},'
    f.write(format % tuple(data))


dataFromPage()
