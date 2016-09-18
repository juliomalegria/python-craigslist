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

Classes
-------

Base class:

* ``CraigslistBase``

Subclasses:

* ``CraigslistCommunity`` (craigslist.org > community)
* ``CraigslistHousing`` (craigslist.org > housing)
* ``CraigslistJobs`` (craigslist.org > jobs)
* ``CraigslistPersonals`` (craigslist.org > personals)
* ``CraigslistForSale`` (craigslist.org > for sale)
* ``CraigslistEvents`` (craigslist.org > event calendar)
* ``CraigslistServices`` (craigslist.org > services)
* ``CraigslistGigs`` (craigslist.org > gigs)
* ``CraigslistResumes`` (craigslist.org > resumes)

Usage
-----

Every subclass has its own set of filters. To get a list of all the filters
supported by a specific subclass, use the ``.show_filters()`` class-method:

.. code:: python

   >>> from craigslist import CraigslistJobs
   >>> CraigslistJobs.show_filters()

   Base filters:
   * posted_today = True/False
   * query = ...
   * search_titles = True/False
   * has_image = True/False
   Section specific filters:
   * is_internship = True/False
   * is_telecommuting = True/False
   * is_contract = True/False
   * is_parttime = True/False
   * is_nonprofit = True/False
   * employment_type = u'full-time', u'part-time', u'contract', u"employee's choice"
 
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

Maybe an engineering internship in Silicon Valley?

.. code:: python

    from craigslist import CraigslistJobs
    cl_j = CraigslistJobs(site='sfbay', area='sby', category='eng',
                          filters={'is_internship': True, 'employment_type': ['full-time', 'part-time']})

    for result in cl_j.get_results():
        print result

    {
        'id': u'5708651182',
        'name': u'GAME DEVELOPER INTERNSHIP AT TYNKER - AVAILABLE NOW!',
	'url': u'http://sfbay.craigslist.org/pen/eng/5708651182.html',
	'datetime': u'2016-07-30 13:30',
	'price': None,
	'where': u'mountain view',
	'has_image': True,
	'has_map': True,
	'geotag': None
    }
    # ...

Events with free food in New York?

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
