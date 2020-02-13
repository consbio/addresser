Addresser
=========

Addresser parses and normalizes street addresses and intersections. It is a port of the Node package,
`parse-address <https://github.com/hassansin/parse-address>`_, which in turn is a port of the PERL package,
`Geo::StreetAddress::US <http://search.cpan.org/~timb/Geo-StreetAddress-US-1.04/US.pm>`_.

From the `Geo::StreetAddress::US` description:

    Geo::StreetAddress::US is a regex-based street address and street intersection parser for the United States. Its
    basic goal is to be as forgiving as possible when parsing user-provided address strings. Geo::StreetAddress::US knows
    about directional prefixes and suffixes, fractional building numbers, building units, grid-based addresses (such as
    those used in parts of Utah), 5 and 9 digit ZIP codes, and all of the official USPS abbreviations for street types
    and state names...

Install
-------

Addresser can be installed from pip:

.. code-block:: text

    $ pip install addresser

Usage
-----

.. code-block:: python

    from addresser import parse_location

    parse_location('1005 N Gravenstein Highway Sebastopol CA 95472')

**Result**

.. code-block:: python

    {
        'number': '1005',
        'prefix': 'N',
        'street': 'Gravenstein',
        'type': 'Hwy',
        'city': 'Sebastopol',
        'state': 'CA',
        'zip': '95472'
    }
