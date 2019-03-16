.. contents:: **humanreadable**
   :backlinks: top
   :depth: 2


Summary
============================================
humanreadable is a Python library to convert from human-readable values to Python values.

- Supported unites:
    - time (days, hours, minutes, seconds, ...)
    - bit per seconds


Usage
============================================

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
        120 sec to msecs -> 120000.0
        120 sec to minutes -> 2.0

        [Examples: humanreadable.BitPerSecond]
        1 Gbps to Mbps -> 1000.0
        1 Gbps to Kbps -> 1000000.0
        1 Gbps to Kibps -> 953674.31640625


Installation
============================================
::

    pip install humanreadable


Dependencies
============================================
Python 2.7+ or 3.4+

- `six <https://pypi.org/project/six/>`__
- `typepy <https://github.com/thombashi/typepy>`__
