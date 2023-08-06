
waterpyk
========

.. image:: https://colab.research.google.com/assets/colab-badge.svg
    :target: https://colab.research.google.com/github/erica-mccormick/waterpyk/blob/main/waterpyk_tutorialL.ipynb
    :alt: open in colab

.. image:: https://readthedocs.org/projects/pip/badge/
    :target: https://waterpyk.readthedocs.io
    :alt: readthedocs badge

.. image:: https://img.shields.io/pypi/v/waterpyk.svg
    :target: https://pypi.python.org/pypi/waterpyk
    :alt: PyPi badge

.. image:: https://img.shields.io/twitter/follow/McCormickEricaL?style=social   	
    :target: https://twitter.com/McCormickEricaL
    :alt: Follow me on Twitter badge

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT license badge

**A python package to analyze hydrological timeseries for a site or watershed using the Google Earth Engine and USGS APIs.**

* GitHub repo: https://github.com/erica-mccormick/waterpyk
* Documentation: https://waterpyk.readthedocs.io/en/latest/
* PyPI: https://pypi.org/project/waterpyk/
* Report bugs: https://github.com/erica-mccormick/waterpyk/issues

waterpyk is a simple package for extracting data from the `Google Earth Engine`_ (GEE) and USGS APIs and performing simple water-balance analyses.
All you need to begin is a lat/long or a `USGS gauge ID`_ to start.

For more information on the root-zone water storage capacity and deficit, see `Dralle et al., 2021`_, `McCormick et al., 2021`_, and `Rempe, McCormick et al. (in prep)`_.

`Check out the tutorial`_ for basic waterpyk usage in GoogleColab here.

Get Started
===========

waterpyk requires `geopandas`_ and ee.
Read the `workflow to install and authenticate ee`_ (GEE) for Google Colab, pip, or conda.
You will need to `sign up for a GEE account`_ if it is your first time.

Install waterpyk::

    pip install waterpyk

To get all of the available data and plots for a site, simply supply a list of coordinates (such as ``[lat, long]`` or [``gaugeID``]).::

    from waterpyk install main

    coords = [LAT/LONG] # or
    gage = [USGS_gage_ID]
    yoursitename = main.StudyArea(COORDS_or_GAGE, layers = 'all')

A note on the ``layers`` parameter:
Two default options are available for extracting data.::
 
    layers = 'all'
    layers = 'minimal'

'All' will extract precipitation (P), evapotranspiration (ET) from MODIS and PML, MODIS snow cover, MODIS landcover class, and SRTM elevation, including all relevant bands.

'Minimal' is the fastest option and extracts only the necessary data for the deficit (P, ET, and snow without extra MODIS products).

Alternatively, ``layers`` can also take a dataframe containing a row for each desired GEE asset. See the main and/or gee module docs for more information.

Note that most GEE assets should be extracted with no errors, however not all date formats have been tested, so new assets may throw errors and require manual extraction outside of waterpyk.
For these cases, I suggest using the `geemap`_ package, which has many fantastic GEE tools and inspired some of this code as well!

Now that you've initialized your StudyArea object, all of the dataframes of extracted data will now be available in the form of::

    yoursitename.daily_df_wide # includes deficit, wateryear deficit, and cumulative wateryear timeseries
    yoursitename.streamflow
    yoursitename.wateryear_totals
    yoursitename.stats

Some single values are also available as attributes in this way,
such as root-zone water storage capacity (Smax, mm) and and mean annual precipitation (MAP, mm)::

    yoursite.smax
    yoursite.MAP

To plot, supply a string for which kind of plot (see below for the 5 options), such as::

    yoursitename.plot(kind = 'timeseries')

Extra keyword arguments are available for the plots to change the color, line types, or included data for each kind. See the plots module for default kwargs.

Docs
====

For full documentation, see `full documentation`_.

What Waterpyk Can Do
=====================

* Download timeseries of GEE assets and:

  * Combining bands

  * Applying a scaling factor

  * Interpolating to daily

* Download streamflow for gauged watersheds

* Download watershed information, such as:

  * Boundary and flowline geometry (as GEE or geopandas format)

  * Metadata (such as CRS, name, and gauge ID)

  * Daily discharge (in native units, and converted to mm)

  * Centroid latitude (for calculation of Hargreaves PET)

  * URLs necessary to access all of the above directly

* Calculate cumulative and total wateryear timeseries

* Calculate the root-zone water storage (RWS) deficit

* Create 4 figures, out of the box, with P, ET, Q, and deficit data, including:
 
  * Wateryear cumulative timeseries (``kind = 'wateryear'``)
 
  * Daily timeseries, with options (``kind = 'timeseries'``)
 
  * Plot & calculate Spearman correlation coefficient for summer ET and wateryear P (``kind = 'spearman'``)
 
  * RWS capacity (Smax) relative to P distribution (``kind = 'distribution'``)
 
  * RWS timeseries (``kind = 'RWS'``)


Contact
=======

This is a work in progress and is primarily intended for the Rempe Lab Group and co-authors.
Feel free to report bugs, and note that major version updates may not be backwards compatible.
For more information, contact Erica McCormick at erica.elmstead@gmail.com or the email address given on her `homepage`_.

.. _Dralle et al., 2021: https://ericamccormick.com/pdfs/Dralle2021_HESS.pdf
.. _Rempe, McCormick et al. (in prep): https://eartharxiv.org/repository/view/3356/
.. _McCormick et al., 2021: https://ericamccormick.com/pdfs/McCormick_Nature2021.pdf
.. _USGS gauge ID: https://waterdata.usgs.gov/nwis/rt
.. _Google Earth Engine: https://developers.google.com/earth-engine/guides/getstarted
.. _homepage: https://www.ericamccormick.com
.. _full documentation: https://waterpyk.readthedocs.io/en/latest/
.. _Check out the tutorial: https://colab.research.google.com/github/erica-mccormick/waterpyk/blob/main/waterpyk_tutorialL.ipynb
.. _geemap: https://github.com/giswqs/geemap
.. _sign up for a GEE account: https://earthengine.google.com/new_signup/
.. _workflow to install and authenticate ee: https://developers.google.com/earth-engine/guides/python_install
.. _geopandas: https://geopandas.org/