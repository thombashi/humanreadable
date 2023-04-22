.. contents:: **humanreadable**
   :backlinks: top
   :depth: 2


Summary
============================================
humanreadable is a Python library to convert human-readable values to other units.

.. image:: https://badge.fury.io/py/humanreadable.svg
    :target: https://badge.fury.io/py/humanreadable
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/humanreadable.svg
   :target: https://pypi.org/project/humanreadable
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/pathvalidate.svg
    :target: https://pypi.org/project/pathvalidate
    :alt: Supported Python implementations

.. image:: https://github.com/thombashi/humanreadable/actions/workflows/lint_and_test.yml/badge.svg
    :target: https://github.com/thombashi/humanreadable/actions/workflows/lint_and_test.yml
    :alt: CI status of Linux/macOS/Windows

.. image:: https://coveralls.io/repos/github/thombashi/humanreadable/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/humanreadable?branch=master
    :alt: Test coverage


Supported Unites
-------------------------------------------
- time (days, hours, minutes, seconds, etc.)
- bits per second


Usage
============================================

Convert a human-readable value to another unit
----------------------------------------------
:Sample Code:
    .. code-block:: python

        import humanreadable as hr

        print("\n[Examples: humanreadable.Time]")
        value = "120 sec"
        print("'{}' to msecs -> {}".format(value, hr.Time(value).milliseconds))
        print("'{}' to minutes -> {}".format(value, hr.Time(value).minutes))

        value = "12 min 40 sec"
        print("'{}' to seconds -> {}".format(value, hr.Time(value).seconds))

        print("\n[Examples: humanreadable.BitsPerSecond]")
        value = "1 Gbps"
        print("'{}' to Mbps -> {}".format(value, hr.BitsPerSecond(value).mega_bps))
        print("'{}' to Kbps -> {}".format(value, hr.BitsPerSecond(value).kilo_bps))
        print("'{}' to Kibps -> {}".format(value, hr.BitsPerSecond(value).kibi_bps))

:Output:
    .. code-block::

        [Examples: humanreadable.Time]
        '120 sec' to msecs -> 120000.0
        '120 sec' to minutes -> 2.0
        '12 minutes 40 seconds' to seconds -> 760.0

        [Examples: humanreadable.BitsPerSecond]
        '1 Gbps' to Mbps -> 1000.0
        '1 Gbps' to Kbps -> 1000000.0
        '1 Gbps' to Kibps -> 976562.5


Convert a value to a human readable string
----------------------------------------------
:Sample Code:
    .. code-block:: python

        import humanreadable as hr

        hr.Time("400", default_unit=hr.Time.Unit.SECOND).to_humanreadable()

:Output:
    .. code-block::

        6 minutes 40 seconds

Set default unit
-------------------------------------------
Unit for an instance is determined by input value.
If a valid unit is not found, ``default_unit`` will be used for the instance (defaults to ``None``).

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

.. table:: Available units for ``humanreadable.BitsPerSecond``

    +-----+-----------------------------+
    |Unit |Available specifiers (str)   |
    +=====+=============================+
    |bps  |``bps``/``bits?/s``          |
    +-----+-----------------------------+
    |Kbps |``[kK]bps``/``[kK]bits?/s``  |
    +-----+-----------------------------+
    |Kibps|``[kK]ibps``/``[kK]ibits?/s``|
    +-----+-----------------------------+
    |Mbps |``[mM]bps``/``[mM]bits?/s``  |
    +-----+-----------------------------+
    |Mibps|``[mM]ibps``/``[mM]ibits?/s``|
    +-----+-----------------------------+
    |Gbps |``[gG]bps``/``[gG]bits?/s``  |
    +-----+-----------------------------+
    |Gibps|``[gG]ibps``/``[gG]ibits?/s``|
    +-----+-----------------------------+
    |Tbps |``[tT]bps``/``[tT]bits?/s``  |
    +-----+-----------------------------+
    |Tibps|``[tT]ibps``/``[tT]ibits?/s``|
    +-----+-----------------------------+


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
- Python 3.6+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/humanreadable/network/dependencies>`__
