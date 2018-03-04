from bs4 import BeautifulSoup
import requests

ALL_SITES_URL = 'http://www.craigslist.org/about/sites'
SITE_URL = 'http://%s.craigslist.org'


def get_all_sites():
    response = requests.get(ALL_SITES_URL)
    response.raise_for_status()  # Something failed?
    soup = BeautifulSoup(response.content, 'html.parser')
    sites = set()

    for box in soup.findAll('div', {'class': 'box'}):
        for a in box.findAll('a'):
            # Remove protocol and get subdomain
            site = a.attrs['href'].rsplit('//', 1)[1].split('.')[0]
            sites.add(site)

    return sites


def get_all_areas(site):
    response = requests.get(SITE_URL % site)
    response.raise_for_status()  # Something failed?
    soup = BeautifulSoup(response.content, 'html.parser')
    raw = soup.select('ul.sublinks li a')
    sites = set(a.attrs['href'].rsplit('/')[1] for a in raw)
    return sites
