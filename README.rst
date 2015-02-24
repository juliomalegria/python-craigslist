python-craigslist
=================

A simple `Craigslist <http://www.craigslist.org>`__ wrapper.

License: `MIT-Zero <https://romanrm.net/mit-zero>`__.

Disclaimer
----------

* I don't work for or have any affiliation with Craigslist.
* This module was implemented for educational purposes. It should not be used for crawling or downloading data from Craigslist.

Installation
------------

::

    pip install python-craigslist

Classes and its options
-----------------------

Base class:

::

    CraigslistBase
    ├── query         (String)
    ├── search_titles (True or False)
    ├── has_image     (True or False)
    └── posted_today  (True or False)

Subclasses (include all base class options):

::

    CraigslistCommunity
    └── $

    CraigslistEvents
    ├── art          (True of False)
    ├── athletics    (True of False)
    ├── career       (True of False)
    ├── dance        (True of False)
    ├── festival     (True of False)
    ├── fitness      (True of False)
    ├── health       (True of False)
    ├── food         (True of False)
    ├── drink        (True of False)
    ├── free         (True of False)
    ├── fundraiser   (True of False)
    ├── tech         (True of False)
    ├── kid_friendly (True of False)
    ├── literacy     (True of False)
    ├── music        (True of False)
    ├── outdoor      (True of False)
    ├── sale         (True of False)
    └── singles      (True of False)

    CraigslistForSale
    ├── min_price (Number)
    ├── max_price (Number)
    ├── make      (String)
    ├── model     (String)
    ├── min_year  (Number)
    ├── max_year  (Number)
    ├── min_miles (Number)
    └── max_miles (Number)

    CraigslistGigs
    └── is_paid (True of False)

    CraigslistHousing
    ├── private_room (True of False)
    ├── private_bath (True of False)
    ├── cats_ok      (True of False)
    ├── dogs_ok      (True of False)
    ├── min_price    (Number)
    ├── max_price    (Number)
    ├── min_ft2      (Number)
    └── max_ft2      (Number)

    CraigslistJobs
    └── $

    CraigslistPersonals
    ├── min_age (Number)
    └── max_age (Number)

    CraigslistResumes
    └── $

    CraigslistServices
    └── $

Examples
--------

Looking for a room in San Francisco?

.. code:: python

    from craigslist import CraigslistHousing

    cl_h = CraigslistHousing(site='sfbay', area='sfc', category='roo',
                             filters={'max_price': 1200, 'private_room': True})

    for result in cl_h.get_results(sort_by='newest', geotagged=True):
        print result

    {
        'id': u'4851150747',
        'name': u'Near SFSU, UCSF and NEWLY FURNISHED - CLEAN, CONVENIENT and CLEAN!',
        'url': u'http://sfbay.craigslist.org/sfc/roo/4851150747.html',
        'datetime': u'2015-01-27 23:44',
        'price': u'$1100',
        'where': u'inner sunset / UCSF',
        'has_image': False,
        'has_map': True,
        'geotag': (37.738473, -122.494721)
    }
    # ...

Everyone loves free food!

.. code:: python

    from craigslist import CraigslistEvents

    cl_e = CraigslistEvents(site='newyork', filters={'free': True, 'food': True})

    for result in cl_e.get_results(sort_by='newest', limit=5):
        print result

    {
        'id': u'4866178242',
        'name': u'Lituation Thursdays @ Le Reve',
        'url': u'http://newyork.craigslist.org/mnh/eve/4866178242.html',
        'datetime': u'1/29',
        'price': None,
        'where': u'Midtown East',
        'has_image': True,
        'has_map': True,
        'geotag': None
    }
    # ...

Support
-------

If you find any bug or you want to propose a new feature, please use the `issues tracker <https://github.com/juliomalegria/python-craigslist/issues>`__. I'll be happy to help you! :-)
