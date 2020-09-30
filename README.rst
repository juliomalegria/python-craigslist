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
* ``CraigslistForSale`` (craigslist.org > for sale)
* ``CraigslistEvents`` (craigslist.org > event calendar)
* ``CraigslistServices`` (craigslist.org > services)
* ``CraigslistGigs`` (craigslist.org > gigs)
* ``CraigslistResumes`` (craigslist.org > resumes)

Examples
--------

Looking for a room in San Francisco?

.. code:: python

    from craigslist import CraigslistHousing
    cl_h = CraigslistHousing(site='sfbay', area='sfc', category='roo',
                             filters={'max_price': 1200, 'private_room': True})

    # You can get an approximate amount of results with the following call:
    print(cl_h.get_results_approx_count())

    992

    for result in cl_h.get_results(sort_by='newest', geotagged=True):
        print(result)

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

Maybe a software engineering internship in Silicon Valley?

.. code:: python

    from craigslist import CraigslistJobs
    cl_j = CraigslistJobs(site='sfbay', area='sby', category='sof',
                          filters={'is_internship': True, 'employment_type': ['full-time', 'part-time']})

    for result in cl_j.get_results():
        print(result)

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
        print(result)

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

Where to get `filters` from?
----------------------------

Every subclass has its own set of filters. To get a list of all the filters
supported by a specific subclass, use the ``.show_filters()`` class-method:

.. code:: python

   >>> from craigslist import CraigslistJobs, CraigslistForSale
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

   >>> CraigslistForSale.show_filters(category='cta')

   Base filters:
   * posted_today = True/False
   * query = ...
   * search_titles = True/False
   * has_image = True/False
   Section specific filters:
   * min_year = ...
   * model = ...
   * min_price = ...
   * max_miles = ...
   * make = ...
   * max_price = ...
   * min_miles = ...
   * max_year = ...
   * auto_title_status = u'clean', u'salvage', u'rebuilt', u'parts only', u'lien', u'missing'
   * auto_transmission = u'manual', u'automatic', u'other'
   * auto_fuel_type = u'gas', u'diesel', u'hybrid', u'electric', u'other'
   * auto_paint = u'black', u'blue', u'brown', u'green', u'grey', u'orange', u'purple', u'red', u'silver', u'white', u'yellow', u'custom'
   * auto_bodytype = u'bus', u'convertible', u'coupe', u'hatchback', u'mini-van', u'offroad', u'pickup', u'sedan', u'truck', u'SUV', u'wagon', u'van', u'other'
   * auto_drivetrain = u'fwd', u'rwd', u'4wd'
   * auto_size = u'compact', u'full-size', u'mid-size', u'sub-compact'
   * auto_cylinders = u'3 cylinders', u'4 cylinders', u'5 cylinders', u'6 cylinders', u'8 cylinders', u'10 cylinders', u'12 cylinders', u'other'
   * condition = u'new', u'like new', u'excellent', u'good', u'fair', u'salvage'

Where to get ``site`` and ``area`` from?
----------------------------------------

When initializing any of the subclasses, you'll need to provide the ``site``, and optionall the ``area``, from where you want to query data.

To get the correct ``site``, follow these steps:

1. Go to `craigslist.org/about/sites <https://www.craigslist.org/about/sites>`__.
2. Find the country or city you're interested on, and click on it.
3. You'll be directed to ``<site>.craigslist.org``. The value of ``<site>`` in the URL is the one you should use.

Not all sites have areas. To check if your site has areas, check for links next to the title of the Craigslist page, on the top center. For example, for New York you'll see:

.. image:: https://user-images.githubusercontent.com/1008637/45307206-bb404d80-b51e-11e8-8e6d-edfbdbd0a6fa.png

Click on the one you're interested, and you'll be redirected to ``<site>.craigslist.org/<area>``. The value of ``<area>`` in the URL is the one you should use. If there are no areas next to the title, it means your site has no areas, and you can leave that argument unset.

Where to get ``category`` from?
-------------------------------

You can additionally provide a ``category`` when initializing any of the subclasses. To obtain the code of this ``category``, follow these steps:

1. Go to ``<site>.craigslist.org`` or just `craigslist.org <https://www.craigslist.org>`__ (you'll be directed to the last used ``site``).
2. You'll see a list of categories and subcategories (see image below).
3. Click on the interested subcategory. You'll be redirected to the search view for that subcategory. The URL you were redirected will end with ``/search/<category>``. This would be the code for your category.

.. image:: https://user-images.githubusercontent.com/14173022/46252889-3614ce00-c424-11e8-9bac-060c236b8b58.png

Is there a limit for the number of results?
--------------------------------------------

Yes, Craigslist caps the results for any search to 3000.

Support
-------

If you find any bug or you want to propose a new feature, please use the `issues tracker <https://github.com/juliomalegria/python-craigslist/issues>`__. I'll be happy to help you! :-)
