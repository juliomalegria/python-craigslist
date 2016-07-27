from bs4 import BeautifulSoup
import logging
try:
    from Queue import Queue  # PY2
except ImportError:
    from queue import Queue  # PY3
import requests
from requests.exceptions import RequestException
from six import iteritems
from threading import Thread
try:
    from urlparse import urljoin  # PY2
except ImportError:
    from urllib.parse import urljoin  # PY3

from .sites import get_all_sites

ALL_SITES = get_all_sites()  # All the Craiglist sites
RESULTS_PER_REQUEST = 100  # Craigslist returns 100 results per request


def requests_get(*args, **kwargs):
    """
    Retries if a RequestException is raised (could be a connection error or
    a timeout).
    """

    logger = kwargs.pop('logger', None)
    try:
        return requests.get(*args, **kwargs)
    except RequestException as exc:
        if logger:
            logger.warning('Request failed (%s). Retrying ...', exc)
        return requests.get(*args, **kwargs)


class CraigslistBase(object):
    """ Base class for all Craiglist wrappers. """

    url_templates = {
        'base': 'http://%(site)s.craigslist.org',
        'no_area': 'http://%(site)s.craigslist.org/search/%(category)s',
        'area': 'http://%(site)s.craigslist.org/search/%(area)s/%(category)s'
    }

    default_category = None

    base_filters = {
        'query': {'url_key': 'query', 'value': None},
        'search_titles': {'url_key': 'srchType', 'value': 'T'},
        'has_image': {'url_key': 'hasPic', 'value': 1},
        'posted_today': {'url_key': 'postedToday', 'value': 1},
    }
    extra_filters = {}

    sort_by_options = {
        'newest': 'date',
        'price_asc': 'priceasc',
        'price_desc': 'pricedsc',
    }

    def __init__(self, site='sfbay', area=None, category=None, filters=None,
                 log_level=logging.WARNING):
        # Logging
        self.set_logger(log_level, init=True)

        if site not in ALL_SITES:
            msg = "'%s' is not a valid site" % site
            self.logger.error(msg)
            raise ValueError(msg)
        self.site = site

        if area:
            base_url = self.url_templates['base']
            response = requests_get(base_url % {'site': self.site},
                                    logger=self.logger)
            soup = BeautifulSoup(response.content, 'html.parser')
            sublinks = soup.find('ul', {'class': 'sublinks'})
            if not sublinks or not sublinks.find('a', text=area):
                msg = "'%s' is not a valid area for site '%s'" % (area, site)
                self.logger.error(msg)
                raise ValueError(msg)
        self.area = area

        self.category = category or self.default_category

        url_template = self.url_templates['area' if area else 'no_area']
        self.url = url_template % {'site': self.site, 'area': self.area,
                                   'category': self.category}

        self.filters = {}
        for key, value in iteritems((filters or {})):
            try:
                filter = self.base_filters.get(key) or self.extra_filters[key]
                self.filters[filter['url_key']] = filter['value'] or value
            except KeyError:
                self.logger.warning("'%s' is not a valid filter", key)

    def set_logger(self, log_level, init=False):
        if init:
            self.logger = logging.getLogger('python-craiglist')
            self.handler = logging.StreamHandler()
            self.logger.addHandler(self.handler)
        self.logger.setLevel(log_level)
        self.handler.setLevel(log_level)

    def get_results(self, limit=None, sort_by=None, geotagged=False):
        """
        Get results from Craigslist based on the specified filters.

        If geotagged=True, the results will include the (lat, lng) in the
        'geotag' attrib (this will make the process a little bit longer).
        """

        if sort_by:
            try:
                self.filters['sort'] = self.sort_by_options[sort_by]
            except KeyError:
                msg = ("'%s' is not a valid sort_by option, "
                       "use: 'newest', 'price_asc' or 'price_desc'" % sort_by)
                self.logger.error(msg)
                raise ValueError(msg)

        start = 0
        total_so_far = 0
        total = 0

        while True:
            self.filters['s'] = start
            response = requests_get(self.url, params=self.filters,
                                    logger=self.logger)
            self.logger.info('GET %s', response.url)
            self.logger.info('Response code: %s', response.status_code)
            response.raise_for_status()  # Something failed?

            soup = BeautifulSoup(response.content, 'html.parser')
            if not total:
                totalcount = soup.find('span', {'class': 'totalcount'})
                total = int(totalcount.text) if totalcount else 0

            for row in soup.find_all('p', {'class': 'row'}):
                if limit is not None and total_so_far >= limit:
                    break
                self.logger.debug('Processing %s of %s results ...',
                                  total_so_far + 1, total)

                link = row.find('a', {'class': 'hdrlnk'})
                id = link.attrs['data-id']
                name = link.text
                url = urljoin(self.url, link.attrs['href'])

                time = row.find('time')
                if time:
                    datetime = time.attrs['datetime']
                else:
                    pl = row.find('span', {'class': 'pl'})
                    datetime = pl.text.split(':')[0].strip() if pl else None
                price = row.find('span', {'class': 'price'})
                where = row.find('small')
                p_text = row.find('span', {'class': 'p'}).text

                result = {'id': id,
                          'name': name,
                          'url': url,
                          'datetime': datetime,
                          'price': price.text if price else None,
                          'where': where.text.strip('() ') if where else None,
                          'has_image': 'pic' in p_text,
                          'has_map': 'map' in p_text,
                          'geotag': None}

                if geotagged:
                    self.geotag_result(result)

                yield result
                total_so_far += 1

            if total_so_far == limit:
                break
            if (total_so_far - start) < RESULTS_PER_REQUEST:
                break
            start = total_so_far

    def geotag_result(self, result):
        """ Adds (lat, lng) to result. """

        self.logger.debug('Geotagging result ...')

        if result['has_map']:
            response = requests_get(result['url'], logger=self.logger)
            self.logger.info('GET %s', response.url)
            self.logger.info('Response code: %s', response.status_code)

            if response.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
                map = soup.find('div', {'id': 'map'})
                if map:
                    result['geotag'] = (float(map.attrs['data-latitude']),
                                        float(map.attrs['data-longitude']))

        return result

    def geotag_results(self, results, workers=8):
        """
        Add (lat, lng) to each result. This process is done using N threads,
        where N is the amount of workers defined (default: 8).
        """

        results = list(results)
        queue = Queue()

        for result in results:
            queue.put(result)

        def geotagger():
            while not queue.empty():
                self.logger.debug('%s results left to geotag ...',
                                  queue.qsize())
                self.geotag_result(queue.get())
                queue.task_done()

        threads = []
        for _ in xrange(workers):
            thread = Thread(target=geotagger)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        return results


class CraigslistCommunity(CraigslistBase):
    """ Craigslist community wrapper. """

    default_category = 'ccc'


class CraigslistEvents(CraigslistBase):
    """ Craigslist events wrapper. """

    default_category = 'eee'

    extra_filters = {
        'art': {'url_key': 'event_art', 'value': 1},
        'athletics': {'url_key': 'event_athletics', 'value': 1},
        'career': {'url_key': 'event_career', 'value': 1},
        'dance': {'url_key': 'event_dance', 'value': 1},
        'festival': {'url_key': 'event_festical', 'value': 1},
        'fitness': {'url_key': 'event_fitness_wellness', 'value': 1},
        'health': {'url_key': 'event_fitness_wellness', 'value': 1},
        'food': {'url_key': 'event_food', 'value': 1},
        'drink': {'url_key': 'event_food', 'value': 1},
        'free': {'url_key': 'event_free', 'value': 1},
        'fundraiser': {'url_key': 'event_fundraiser_vol', 'value': 1},
        'tech': {'url_key': 'event_geek', 'value': 1},
        'kid_friendly': {'url_key': 'event_kidfriendly', 'value': 1},
        'literacy': {'url_key': 'event_literacy', 'value': 1},
        'music': {'url_key': 'event_music', 'value': 1},
        'outdoor': {'url_key': 'event_outdoor', 'value': 1},
        'sale': {'url_key': 'event_sale', 'value': 1},
        'singles': {'url_key': 'event_singles', 'value': 1},
    }


class CraigslistForSale(CraigslistBase):
    """ Craigslist for sale wrapper. """

    default_category = 'sss'

    extra_filters = {
        'min_price': {'url_key': 'minAsk', 'value': None},
        'max_price': {'url_key': 'maxAsk', 'value': None},
        'make': {'url_key': 'autoMakeModel', 'value': None},
        'model': {'url_key': 'autoMakeModel', 'value': None},
        'min_year': {'url_key': 'autoMinYear', 'value': None},
        'max_year': {'url_key': 'autoMaxYear', 'value': None},
        'min_miles': {'url_key': 'autoMilesMin', 'value': None},
        'max_miles': {'url_key': 'autoMilesMax', 'value': None},
    }


class CraigslistGigs(CraigslistBase):
    """ Craigslist gigs wrapper. """

    default_category = 'ggg'

    extra_filters = {
        'is_paid': {'url_key': 'is_paid', 'value': None},
    }

    def __init__(self, *args, **kwargs):
        try:
            is_paid = kwargs['filters']['is_paid']
            kwargs['filters']['is_paid'] = 'yes' if is_paid else 'no'
        except KeyError:
            pass
        super(CraigslistGigs, self).__init__(*args, **kwargs)


class CraigslistHousing(CraigslistBase):
    """ Craigslist housing wrapper. """

    default_category = 'hhh'

    extra_filters = {
        'private_room': {'url_key': 'private_room', 'value': 1},
        'private_bath': {'url_key': 'private_bath', 'value': 1},
        'cats_ok': {'url_key': 'pets_cat', 'value': 1},
        'dogs_ok': {'url_key': 'pets_dog', 'value': 1},
        'min_price': {'url_key': 'minAsk', 'value': None},
        'max_price': {'url_key': 'maxAsk', 'value': None},
        'min_ft2': {'url_key': 'minSqft', 'value': None},
        'max_ft2': {'url_key': 'maxSqft', 'value': None},
        'search_distance': {'url_key': 'search_distance', 'value': None},
        'zip_code': {'url_key': 'postal', 'value': None},
        'bedrooms': {'url_key': 'bedrooms', 'value': None},
        'bathrooms': {'url_key': 'bathrooms', 'value': None},
        'laundry_in_unit': {'url_key': 'laundry', 'value': 1},
        'no_smoking': {'url_key': 'no_smoking', 'value': 1},
    }


class CraigslistJobs(CraigslistBase):
    """ Craigslist jobs wrapper. """

    default_category = 'jjj'

    extra_filters = {
        'is_contract': {'url_key': 'is_contract', 'value': 1},
        'is_internship': {'url_key': 'is_internship', 'value': 1},
        'is_nonprofit': {'url_key': 'is_nonprofit', 'value': 1},
        'is_parttime': {'url_key': 'is_parttime', 'value': 1},
        'is_telecommuting': {'url_key': 'is_telecommuting', 'value': 1},
    }


class CraigslistPersonals(CraigslistBase):
    """ Craigslist personals wrapper. """

    default_category = 'ppp'

    extra_filters = {
        'min_age': {'url_key': 'minAsk', 'value': None},
        'max_age': {'url_key': 'maxAsk', 'value': None},
    }


class CraigslistResumes(CraigslistBase):
    """ Craigslist resumes wrapper. """

    default_category = 'rrr'


class CraigslistServices(CraigslistBase):
    """ Craigslist services wrapper. """

    default_category = 'bbb'
