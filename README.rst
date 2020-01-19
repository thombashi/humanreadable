.. contents:: **humanreadable**
   :backlinks: top
   :depth: 2


Summary
============================================
humanreadable is a Python library to convert from human-readable values to other units.

.. image:: https://badge.fury.io/py/humanreadable.svg
    :target: https://badge.fury.io/py/humanreadable
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/humanreadable.svg
   :target: https://pypi.org/project/humanreadable
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/pathvalidate.svg
    :target: https://pypi.org/project/pathvalidate
    :alt: Supported Python implementations

.. image:: https://img.shields.io/travis/thombashi/humanreadable/master.svg?label=Linux/macOS%20CI
    :target: https://travis-ci.org/thombashi/humanreadable
    :alt: Linux/macOS CI status

.. image:: https://img.shields.io/appveyor/ci/thombashi/humanreadable/master.svg?label=Windows%20CI
    :target: https://ci.appveyor.com/project/thombashi/humanreadable

.. image:: https://coveralls.io/repos/github/thombashi/humanreadable/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/humanreadable?branch=master
    :alt: Test coverage


Supported Unites
-------------------------------------------
- time (days, hours, minutes, seconds, etc.)
- bit per seconds


Usage
============================================

Basic usages
-------------------------------------------
:Sample Code:
    .. code-block:: python

        import humanreadable as hr

        print("\n[Examples: humanreadable.Time]")
        value = "120 sec"
        print("'{}' to msecs -> {}".format(value, hr.Time(value).milliseconds))
        print("'{}' to minutes -> {}".format(value, hr.Time(value).minutes))

        print("\n[Examples: humanreadable.BitPerSecond]")
        value = "1 Gbps"
        print("'{}' to Mbps -> {}".format(value, hr.BitPerSecond(value).mega_bps))
        print("'{}' to Kbps -> {}".format(value, hr.BitPerSecond(value).kilo_bps))
        print("'{}' to Kibps -> {}".format(value, hr.BitPerSecond(value).kibi_bps))

:Output:
    .. code-block::

        [Examples: humanreadable.Time]
        '120 sec' to msecs -> 120000.0
        '120 sec' to minutes -> 2.0

        [Examples: humanreadable.BitPerSecond]
        '1 Gbps' to Mbps -> 1000.0
        '1 Gbps' to Kbps -> 1000000.0
        '1 Gbps' to Kibps -> 953674.31640625


Set default unit
-------------------------------------------
Unit for an instance is determined by input value.
If a valid unit not found, ``default_unit``
will be used for the instance (defaults to ``None``).

:Sample Code:
    .. code-block:: python

        import humanreadable as hr

        print(hr.Time("1", default_unit=hr.Time.Unit.SECOND))

:Output:
    .. code-block::

        1.0 seconds


Units
-------------------------------------------
.. table:: Available units for ``humanreadable.Time``

    +------------+----------------------------------------------------------+
    |    Unit    |                Available specifiers (str)                |
    +============+==========================================================+
    |days        |``d``/``day``/``days``                                    |
    +------------+----------------------------------------------------------+
    |hours       |``h``/``hour``/``hours``                                  |
    +------------+----------------------------------------------------------+
    |minutes     |``m``/``min``/``mins``/``minute``/``minutes``             |
    +------------+----------------------------------------------------------+
    |seconds     |``s``/``sec``/``secs``/``second``/``seconds``             |
    +------------+----------------------------------------------------------+
    |milliseconds|``ms``/``msec``/``msecs``/``millisecond``/``milliseconds``|
    +------------+----------------------------------------------------------+
    |microseconds|``us``/``usec``/``usecs``/``microsecond``/``microseconds``|
    +------------+----------------------------------------------------------+

.. table:: Available units for ``humanreadable.BitPerSecond``

    +-----+---------------------------+
    |Unit |Available specifiers (str) |
    +=====+===========================+
    |bps  |``bps``/``bit/s``          |
    +-----+---------------------------+
    |Kbps |``[kK]bps``/``[kK]bit/s``  |
    +-----+---------------------------+
    |Kibps|``[kK]ibps``/``[kK]ibit/s``|
    +-----+---------------------------+
    |Mbps |``[mM]bps``/``[mM]bit/s``  |
    +-----+---------------------------+
    |Mibps|``[mM]ibps``/``[mM]ibit/s``|
    +-----+---------------------------+
    |Gbps |``[gG]bps``/``[gG]bit/s``  |
    +-----+---------------------------+
    |Gibps|``[gG]ibps``/``[gG]ibit/s``|
    +-----+---------------------------+
    |Tbps |``[tT]bps``/``[tT]bit/s``  |
    +-----+---------------------------+
    |Tibps|``[tT]ibps``/``[tT]ibit/s``|
    +-----+---------------------------+


Installation
============================================
Installation: pip
------------------------------
::

    pip install humanreadable

Installation: apt (for Ubuntu)
------------------------------
::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install python3-humanreadable


Dependencies
============================================
Python 2.7+ or 3.5+

- `six <https://pypi.org/project/six/>`__
- `typepy <https://github.com/thombashi/typepy>`__
