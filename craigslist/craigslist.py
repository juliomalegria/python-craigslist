from .base import CraigslistBase


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


class CraigslistResumes(CraigslistBase):
    """ Craigslist resumes wrapper. """

    default_category = 'rrr'


class CraigslistServices(CraigslistBase):
    """ Craigslist services wrapper. """

    default_category = 'bbb'
