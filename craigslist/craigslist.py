from .base import CraigslistBase


class CraigslistCommunity(CraigslistBase):
    """ Craigslist community wrapper. """

    default_category = 'ccc'


class CraigslistEvents(CraigslistBase):
    """ Craigslist events wrapper. """

    default_category = 'eee'

    extra_filters = {
        # art/film
        'art': {'url_key': 'event_art', 'value': 1},
        'film': {'url_key': 'event_art', 'value': 1},
        # career
        'career': {'url_key': 'event_career', 'value': 1},
        # charitable
        'charitable': {'url_key': 'event_fundraiser_vol', 'value': 1},
        'fundraiser': {'url_key': 'event_fundraiser_vol', 'value': 1},
        # competiton
        'athletics': {'url_key': 'event_athletics', 'value': 1},
        'competition': {'url_key': 'event_athletics', 'value': 1},
        # dance
        'dance': {'url_key': 'event_dance', 'value': 1},
        # fest/fair
        'festival': {'url_key': 'event_festival', 'value': 1},
        'fair': {'url_key': 'event_festival', 'value': 1},
        # fitness/health
        'fitness': {'url_key': 'event_fitness_wellness', 'value': 1},
        'health': {'url_key': 'event_fitness_wellness', 'value': 1},
        # food/drink
        'food': {'url_key': 'event_food', 'value': 1},
        'drink': {'url_key': 'event_food', 'value': 1},
        # free
        'free': {'url_key': 'event_free', 'value': 1},
        # kid friendly
        'kid_friendly': {'url_key': 'event_kidfriendly', 'value': 1},
        # literary
        'literary': {'url_key': 'event_literary', 'value': 1},
        # music
        'music': {'url_key': 'event_music', 'value': 1},
        # outdoor
        'outdoor': {'url_key': 'event_outdoor', 'value': 1},
        # sale
        'sale': {'url_key': 'event_sale', 'value': 1},
        # singles
        'singles': {'url_key': 'event_singles', 'value': 1},
        # tech
        'tech': {'url_key': 'event_geek', 'value': 1},
    }


class CraigslistForSale(CraigslistBase):
    """ Craigslist for sale wrapper. """

    default_category = 'sss'

    extra_filters = {
        # price
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        # make and model
        'make': {'url_key': 'auto_make_model', 'value': None},
        'model': {'url_key': 'auto_make_model', 'value': None},
        # model year
        'min_year': {'url_key': 'min_auto_year', 'value': None},
        'max_year': {'url_key': 'max_auto_year', 'value': None},
        # odometer
        'min_miles': {'url_key': 'min_auto_miles', 'value': None},
        'max_miles': {'url_key': 'max_auto_miles', 'value': None},
        # engine displacement (cc)
        'min_engine_displacement': {
            'url_key': 'min_engine_displacement_cc', 'value': None},
        'max_engine_displacement': {
            'url_key': 'max_engine_displacement_cc', 'value': None},
    }


class CraigslistGigs(CraigslistBase):
    """ Craigslist gigs wrapper. """

    default_category = 'ggg'

    extra_filters = {
        # paid/unpaid
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
        # price
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        # bedrooms
        'min_bedrooms': {'url_key': 'min_bedrooms', 'value': None},
        'max_bedrooms': {'url_key': 'max_bedrooms', 'value': None},
        # bathrooms
        'min_bathrooms': {'url_key': 'min_bathrooms', 'value': None},
        'max_bathrooms': {'url_key': 'max_bathrooms', 'value': None},
        # ft2
        'min_ft2': {'url_key': 'minSqft', 'value': None},
        'max_ft2': {'url_key': 'maxSqft', 'value': None},
        # private room
        'private_room': {'url_key': 'private_room', 'value': 1},
        # private bath
        'private_bath': {'url_key': 'private_bath', 'value': 1},
        # cats ok
        'cats_ok': {'url_key': 'pets_cat', 'value': 1},
        # dogs ok
        'dogs_ok': {'url_key': 'pets_dog', 'value': 1},
        # furnished
        'is_furnished': {'url_key': 'is_furnished', 'value': 1},
        # no smoking
        'no_smoking': {'url_key': 'no_smoking', 'value': 1},
        # wheelchair access
        'wheelchair_acccess': {'url_key': 'wheelchaccess', 'value': 1},
        # EV charging
        'ev_charging': {'url_key': 'ev_charging', 'value': 1},
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
        # intership
        'is_internship': {'url_key': 'is_internship', 'value': 1},
        # non-profit
        'is_nonprofit': {'url_key': 'is_nonprofit', 'value': 1},
        # telecommute
        'is_telecommuting': {'url_key': 'is_telecommuting', 'value': 1},
    }


class CraigslistResumes(CraigslistBase):
    """ Craigslist resumes wrapper. """

    default_category = 'rrr'

    extra_filters = {
        # TODO: Please create an issue or PR if interested in this category.
    }


class CraigslistServices(CraigslistBase):
    """ Craigslist services wrapper. """

    default_category = 'bbb'
