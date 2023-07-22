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

.. image:: https://img.shields.io/pypi/implementation/humanreadable.svg
    :target: https://pypi.org/project/humanreadable
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
        print(f"'{value}' to msecs -> {hr.Time(value).milliseconds}")
        print(f"'{value}' to minutes -> {hr.Time(value).minutes}")

        value = "12 min 40 sec"
        print(f"'{value}' to seconds -> {hr.Time(value).seconds}")

        print("\n[Examples: humanreadable.BitsPerSecond]")
        value = "1 Gbps"
        print(f"'{value}' to Mbps -> {hr.BitsPerSecond(value).mega_bps}")
        print(f"'{value}' to Kbps -> {hr.BitsPerSecond(value).kilo_bps}")
        print(f"'{value}' to Kibps -> {hr.BitsPerSecond(value).kibi_bps}")

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

        t = hr.Time("400", default_unit=hr.Time.Unit.SECOND)
        print(t.to_humanreadable())
        print(t.to_humanreadable(style="short"))

:Output:
    .. code-block::

        6 minutes 40 seconds
        6m 40s

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

    +--------------+------------------------------------------------------------+
    |     Unit     |              Available unit specifiers (str)               |
    +==============+============================================================+
    | days         | ``d``/``day``/``days``                                     |
    +--------------+------------------------------------------------------------+
    | hours        | ``h``/``hour``/``hours``                                   |
    +--------------+------------------------------------------------------------+
    | minutes      | ``m``/``min``/``mins``/``minute``/``minutes``              |
    +--------------+------------------------------------------------------------+
    | seconds      | ``s``/``sec``/``secs``/``second``/``seconds``              |
    +--------------+------------------------------------------------------------+
    | milliseconds | ``ms``/``msec``/``msecs``/``millisecond``/``milliseconds`` |
    +--------------+------------------------------------------------------------+
    | microseconds | ``us``/``usec``/``usecs``/``microsecond``/``microseconds`` |
    +--------------+------------------------------------------------------------+

.. table:: Available units for ``humanreadable.BitsPerSecond``

    +-------+--------------------------------------------------------+
    | Unit  |            Available unit specifiers (str)             |
    +=======+========================================================+
    | Kbps  | ``[kK]bps``/``[kK]bits?(/|\s?per\s?)(s|sec|second)``   |
    +-------+--------------------------------------------------------+
    | Kibps | ``[kK]ibps``/``[kK]ibits?(/|\s?per\s?)(s|sec|second)`` |
    +-------+--------------------------------------------------------+
    | Mbps  | ``[mM]bps``/``[mM]bits?(/|\s?per\s?)(s|sec|second)``   |
    +-------+--------------------------------------------------------+
    | Mibps | ``[mM]ibps``/``[mM]ibits?(/|\s?per\s?)(s|sec|second)`` |
    +-------+--------------------------------------------------------+
    | Gbps  | ``[gG]bps``/``[gG]bits?(/|\s?per\s?)(s|sec|second)``   |
    +-------+--------------------------------------------------------+
    | Gibps | ``[gG]ibps``/``[gG]ibits?(/|\s?per\s?)(s|sec|second)`` |
    +-------+--------------------------------------------------------+
    | Tbps  | ``[tT]bps``/``[tT]bits?(/|\s?per\s?)(s|sec|second)``   |
    +-------+--------------------------------------------------------+
    | Tibps | ``[tT]ibps``/``[tT]ibits?(/|\s?per\s?)(s|sec|second)`` |
    +-------+--------------------------------------------------------+
    | bps   | ``bps``/``bits?(/|\s?per\s?)(s|sec|second)``           |
    +-------+--------------------------------------------------------+


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
- Python 3.7+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/humanreadable/network/dependencies>`__
