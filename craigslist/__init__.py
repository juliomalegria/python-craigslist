import logging
try:
    from Queue import Queue  # PY2
except ImportError:
    from queue import Queue  # PY3
from threading import Thread
try:
    from urlparse import urljoin  # PY2
except ImportError:
    from urllib.parse import urljoin  # PY3

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from six import iteritems
from six.moves import range

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


def get_list_filters(url):
    list_filters = {}
    response = requests_get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for list_filter in soup.find_all('div', class_='search-attribute'):
        filter_key = list_filter.attrs['data-attr']
        filter_labels = list_filter.find_all('label')
        options = [opt.text.strip() for opt in filter_labels]
        list_filters[filter_key] = {'url_key': filter_key, 'value': options}
    return list_filters


class CraigslistBase(object):
    """ Base class for all Craiglist wrappers. """

    url_templates = {
        'base': 'http://%(site)s.craigslist.org',
        'no_area': 'http://%(site)s.craigslist.org/search/%(category)s',
        'area': 'http://%(site)s.craigslist.org/search/%(area)s/%(category)s'
    }

    default_site = 'sfbay'
    default_category = None

    base_filters = {
        'query': {'url_key': 'query', 'value': None},
        'search_titles': {'url_key': 'srchType', 'value': 'T'},
        'has_image': {'url_key': 'hasPic', 'value': 1},
        'posted_today': {'url_key': 'postedToday', 'value': 1},
        'search_distance': {'url_key': 'search_distance', 'value': None},
        'zip_code': {'url_key': 'postal', 'value': None},
    }
    extra_filters = {}

    # Set to True to subclass defines the customize_results() method
    custom_result_fields = False

    sort_by_options = {
        'newest': 'date',
        'price_asc': 'priceasc',
        'price_desc': 'pricedsc',
    }

    def __init__(self, site=None, area=None, category=None, filters=None,
                 log_level=logging.WARNING):
        # Logging
        self.set_logger(log_level, init=True)

        self.site = site or self.default_site
        if self.site not in ALL_SITES:
            msg = "'%s' is not a valid site" % self.site
            self.logger.error(msg)
            raise ValueError(msg)

        if area:
            if not self.is_valid_area(area):
                msg = "'%s' is not a valid area for site '%s'" % (area, site)
                self.logger.error(msg)
                raise ValueError(msg)
        self.area = area

        self.category = category or self.default_category

        url_template = self.url_templates['area' if area else 'no_area']
        self.url = url_template % {'site': self.site, 'area': self.area,
                                   'category': self.category}

        list_filters = get_list_filters(self.url)

        self.filters = {}
        for key, value in iteritems((filters or {})):
            try:
                filter = (self.base_filters.get(key) or
                          self.extra_filters.get(key) or
                          list_filters[key])
                if filter['value'] is None:
                    self.filters[filter['url_key']] = value
                elif isinstance(filter['value'], list):
                    valid_options = filter['value']
                    if not hasattr(value, '__iter__'):
                        value = [value]  # Force to list
                    options = []
                    for opt in value:
                        try:
                            options.append(valid_options.index(opt) + 1)
                        except ValueError:
                            self.logger.warning(
                                "'%s' is not a valid option for %s"
                                % (opt, key)
                            )
                    self.filters[filter['url_key']] = options
                elif value:  # Don't add filter if ...=False
                    self.filters[filter['url_key']] = filter['value']
            except KeyError:
                self.logger.warning("'%s' is not a valid filter", key)

    def set_logger(self, log_level, init=False):
        if init:
            self.logger = logging.getLogger('python-craiglist')
            self.handler = logging.StreamHandler()
            self.logger.addHandler(self.handler)
        self.logger.setLevel(log_level)
        self.handler.setLevel(log_level)

    def is_valid_area(self, area):
        base_url = self.url_templates['base']
        response = requests_get(base_url % {'site': self.site},
                                logger=self.logger)
        soup = BeautifulSoup(response.content, 'html.parser')
        sublinks = soup.find('ul', {'class': 'sublinks'})
        return sublinks and sublinks.find('a', text=area) is not None

    def get_results(self, limit=None, start=0, sort_by=None, geotagged=False):
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

        total_so_far = start
        results_yielded = 0
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

            for row in soup.find_all('p', {'class': 'result-info'}):
                if limit is not None and results_yielded >= limit:
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
                price = row.find('span', {'class': 'result-price'})
                where = row.find('span', {'class': 'result-hood'})
                if where:
                    where = where.text.strip()[1:-1]  # remove ()
                tags_span = row.find('span', {'class': 'result-tags'})
                tags = tags_span.text if tags_span else ''

                result = {'id': id,
                          'name': name,
                          'url': url,
                          'datetime': datetime,
                          'price': price.text if price else None,
                          'where': where,
                          'has_image': 'pic' in tags,
                          # TODO: Look into this, looks like all show map now
                          'has_map': 'map' in tags,
                          'geotag': None}

                if self.custom_result_fields:
                    self.customize_result(result, row)

                if geotagged and result['has_map']:
                    self.geotag_result(result)

                yield result
                results_yielded += 1
                total_so_far += 1

            if results_yielded == limit:
                break
            if (total_so_far - start) < RESULTS_PER_REQUEST:
                break
            start = total_so_far

    def customize_result(self, result, html_row):
        """ Add custom/delete/alter fields to result. """
        pass  # Override in subclass to add category-specific fields.

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
        for _ in range(workers):
            thread = Thread(target=geotagger)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        return results

    @classmethod
    def show_filters(cls, category=None):
        print('Base filters:')
        for key, options in iteritems(cls.base_filters):
            value_as_str = '...' if options['value'] is None else 'True/False'
            print('* %s = %s' % (key, value_as_str))
        print('Section specific filters:')
        for key, options in iteritems(cls.extra_filters):
            value_as_str = '...' if options['value'] is None else 'True/False'
            print('* %s = %s' % (key, value_as_str))
        url = cls.url_templates['no_area'] % {
            'site': cls.default_site,
            'category': category or cls.default_category,
        }
        list_filters = get_list_filters(url)
        for key, options in iteritems(list_filters):
            value_as_str = ', '.join([repr(opt) for opt in options['value']])
            print('* %s = %s' % (key, value_as_str))


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
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        'make': {'url_key': 'auto_make_model', 'value': None},
        'model': {'url_key': 'auto_make_model', 'value': None},
        'min_year': {'url_key': 'min_auto_year', 'value': None},
        'max_year': {'url_key': 'max_auto_year', 'value': None},
        'min_miles': {'url_key': 'min_auto_miles', 'value': None},
        'max_miles': {'url_key': 'max_auto_miles', 'value': None},
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
    custom_result_fields = True

    extra_filters = {
        'private_room': {'url_key': 'private_room', 'value': 1},
        'private_bath': {'url_key': 'private_bath', 'value': 1},
        'cats_ok': {'url_key': 'pets_cat', 'value': 1},
        'dogs_ok': {'url_key': 'pets_dog', 'value': 1},
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        'min_ft2': {'url_key': 'minSqft', 'value': None},
        'max_ft2': {'url_key': 'maxSqft', 'value': None},
        'min_bedrooms': {'url_key': 'min_bedrooms', 'value': None},
        'max_bedrooms': {'url_key': 'max_bedrooms', 'value': None},
        'min_bathrooms': {'url_key': 'min_bathrooms', 'value': None},
        'max_bathrooms': {'url_key': 'max_bathrooms', 'value': None},
        'no_smoking': {'url_key': 'no_smoking', 'value': 1},
        'is_furnished': {'url_key': 'is_furnished', 'value': 1},
        'wheelchair_acccess': {'url_key': 'wheelchaccess', 'value': 1},
    }

    def customize_result(self, result, html_row):
        housing_info = html_row.find('span', {'class': 'housing'})
        # Default values
        result.update({'bedrooms': None, 'area': None})
        if housing_info:
            for elem in housing_info.text.split('-'):
                elem = elem.strip()
                if elem.endswith('br'):
                    # Don't convert to int, too risky
                    result['bedrooms'] = elem[:-2]
                if elem.endswith('2'):
                    result['area'] = elem


class CraigslistJobs(CraigslistBase):
    """ Craigslist jobs wrapper. """

    default_category = 'jjj'

    extra_filters = {
        'is_internship': {'url_key': 'is_internship', 'value': 1},
        'is_nonprofit': {'url_key': 'is_nonprofit', 'value': 1},
        'is_telecommuting': {'url_key': 'is_telecommuting', 'value': 1},
    }


class CraigslistPersonals(CraigslistBase):
    """ Craigslist personals wrapper. """

    default_category = 'ppp'

    extra_filters = {
        'min_age': {'url_key': 'min_pers_age', 'value': None},
        'max_age': {'url_key': 'max_pers_age', 'value': None},
    }


class CraigslistResumes(CraigslistBase):
    """ Craigslist resumes wrapper. """

    default_category = 'rrr'


class CraigslistServices(CraigslistBase):
    """ Craigslist services wrapper. """

    default_category = 'bbb'
