python-craigslist
=================

A simple `Craigslist <http://www.craigslist.org>`__ wrapper.

License: `MIT-Zero <https://romanrm.net/mit-zero>`__.

Disclaimer
----------

* I don't work for or have any affiliation with Craigslist.
* This code should not be used for crawling or downloading data from Craigslist.

Classes
-------

* ``CraigslistCommunity``
* ``CraigslistEvents``
* ``CraigslistForSale``
* ``CraigslistGigs``
* ``CraigslistHousing``
* ``CraigslistJobs``
* ``CraigslistPersonals``
* ``CraigslistResumes``
* ``CraigslistServices``

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
