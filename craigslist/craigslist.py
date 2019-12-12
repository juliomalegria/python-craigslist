from .base import CraigslistBase


class CraigslistCommunity(CraigslistBase):
    """ Craigslist community wrapper. """

    default_category = 'ccc'


class CraigslistEvents(CraigslistBase):
    """ Craigslist events wrapper. """

    default_category = 'eee'
    custom_result_fields = True

    extra_filters = {
        # art/film
        'art': {'url_key': 'event_art', 'value': 1, 'attr': 'art/film'},
        'film': {'url_key': 'event_art', 'value': 1, 'attr': 'art/film'},
        # career
        'career': {'url_key': 'event_career', 'value': 1, 'attr': 'career'},
        # charitable
        'charitable': {
            'url_key': 'event_fundraiser_vol', 'value': 1,
            'attr': 'charitable'},
        'fundraiser': {
            'url_key': 'event_fundraiser_vol', 'value': 1,
            'attr': 'charitable'},
        # competiton
        'athletics': {
            'url_key': 'event_athletics', 'value': 1, 'attr': 'competition'},
        'competition': {
            'url_key': 'event_athletics', 'value': 1, 'attr': 'competition'},
        # dance
        'dance': {'url_key': 'event_dance', 'value': 1, 'attr': 'dance'},
        # fest/fair
        'festival': {
            'url_key': 'event_festival', 'value': 1, 'attr': 'fest/fair'},
        'fair': {'url_key': 'event_festival', 'value': 1, 'attr': 'fest/fair'},
        # fitness/health
        'fitness': {
            'url_key': 'event_fitness_wellness', 'value': 1,
            'attr': 'fitness/health'},
        'health': {
            'url_key': 'event_fitness_wellness', 'value': 1,
            'attr': 'fitness/health'},
        # food/drink
        'food': {'url_key': 'event_food', 'value': 1, 'attr': 'food/drink'},
        'drink': {'url_key': 'event_food', 'value': 1, 'attr': 'food/drink'},
        # free
        'free': {'url_key': 'event_free', 'value': 1, 'attr': 'free'},
        # kid friendly
        'kid_friendly': {
            'url_key': 'event_kidfriendly', 'value': 1,
            'attr': 'kid friendly'},
        # literary
        'literary': {
            'url_key': 'event_literary', 'value': 1, 'attr': 'literary'},
        # music
        'music': {'url_key': 'event_music', 'value': 1, 'attr': 'music'},
        # outdoor
        'outdoor': {'url_key': 'event_outdoor', 'value': 1, 'attr': 'outdoor'},
        # sale
        'sale': {'url_key': 'event_sale', 'value': 1, 'attr': 'sale'},
        # singles
        'singles': {'url_key': 'event_singles', 'value': 1, 'attr': 'singles'},
        # tech
        'tech': {'url_key': 'event_geek', 'value': 1, 'attr': 'tech'},
    }

    def customize_result(self, result):
        for attr in result.get('attrs', []):
            # Get venue.
            if attr.lower().startswith('venue: '):
                result['venue'] = attr[7:]


class CraigslistForSale(CraigslistBase):
    """ Craigslist for sale wrapper. """

    default_category = 'sss'
    custom_result_fields = True

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

    def customize_result(self, result):
        for attr in result.get('attrs', []):
            attr_lower = attr.lower()
            # Get miles.
            if attr_lower.startswith('odometer: '):
                result['miles'] = attr[10:]
            # Get engine displacement
            if attr_lower.startswith('engine displacement (cc): '):
                result['engine_displacement'] = attr[26:]


class CraigslistGigs(CraigslistBase):
    """ Craigslist gigs wrapper. """

    default_category = 'ggg'
    custom_result_fields = True

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

    def customize_result(self, result):
        for attr in result.get('attrs', []):
            # Get compensation.
            if attr.lower().startswith('compensation: '):
                result['compensation'] = attr[14:]
        result['is_paid'] = 'compensation' in result


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
        'private_room': {
            'url_key': 'private_room', 'value': 1, 'attr': 'private room'},
        # private bath
        'private_bath': {
            'url_key': 'private_bath', 'value': 1, 'attr': 'private bath'},
        # cats ok
        'cats_ok': {
            'url_key': 'pets_cat', 'value': 1, 'attr': 'cats are ok - purrr'},
        # dogs ok
        'dogs_ok': {
            'url_key': 'pets_dog', 'value': 1, 'attr': 'dogs are ok - wooof'},
        # furnished
        'is_furnished': {
            'url_key': 'is_furnished', 'value': 1, 'attr': 'furnished'},
        # no smoking
        'no_smoking': {
            'url_key': 'no_smoking', 'value': 1, 'attr': 'no smoking'},
        # wheelchair access
        'wheelchair_acccess': {
            'url_key': 'wheelchaccess', 'value': 1,
            'attr': 'wheelchair accessible'},
        # EV charging
        'ev_charging': {
            'url_key': 'ev_charging', 'value': 1, 'attr': 'ev charging'},
        # no appliation fee
        'no_application_fee': {'url_key': 'application_fee', 'value': 1},
        # no broker fee
        'no_broker_fee': {'url_key': 'broker_fee', 'value': 1},
    }

    def customize_result(self, result):
        for attr in result.get('attrs', []):
            attr_lower = attr.lower()
            # Get bedrooms and bathrooms.
            if attr_lower.endswith('br') or attr_lower.endswith('ba'):
                for elem in attr_lower.split(' / '):
                    if elem.endswith('br'):
                        # Don't convert to int, too risky
                        result['bedrooms'] = elem[:-2]
                    elif elem.endswith('ba'):
                        # Don't convert to int, too risky
                        result['bathrooms'] = elem[:-2]
            # Get area.
            elif attr_lower.endswith('ft2') or attr_lower.endswith('m2'):
                result['area'] = attr_lower
            # Get availability.
            elif attr_lower.startswith('available '):
                result['available'] = attr[10:]


class CraigslistJobs(CraigslistBase):
    """ Craigslist jobs wrapper. """

    default_category = 'jjj'
    custom_result_fields = True

    extra_filters = {
        # internship
        'is_internship': {
            'url_key': 'is_internship', 'value': 1, 'attr': 'internship'},
        # non-profit
        'is_nonprofit': {
            'url_key': 'is_nonprofit', 'value': 1,
            'attr': 'non-profit organization'},
        # telecommute
        'is_telecommuting': {
            'url_key': 'is_telecommuting', 'value': 1,
            'attr': 'telecommuting okay'},
    }

    def customize_result(self, result):
        for attr in result.get('attrs', []):
            # Get compensation.
            if attr.lower().startswith('compensation: '):
                result['compensation'] = attr[14:]


class CraigslistResumes(CraigslistBase):
    """ Craigslist resumes wrapper. """

    default_category = 'rrr'

    extra_filters = {
        # TODO: Please create an issue or PR if interested in this category.
    }


class CraigslistServices(CraigslistBase):
    """ Craigslist services wrapper. """

    default_category = 'bbb'
