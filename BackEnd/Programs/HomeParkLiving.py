import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    """
    http://www.homeparkliving.com/home
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    homeObj = soup.find("div", {"id":"sites-canvas-main-content"})
    homeList = homeObj.find("table")
    homeList = homeList.find("table")
    all_homes = []
    counter = 0
    for home in homeList.find_all("tr"):
        if counter > 0:
            homeData = {}
            info = home.find_all("td")
            link = info[0].find("a")
            homeData["Link"] = link['href']
            homeData["Address"] = link.get_text()
            price = info[3].find("font")
            homeData["Price"] = price.get_text()
            print(homeData)
            all_homes.append(homeData)
        counter += 1

    return(all_homes)
