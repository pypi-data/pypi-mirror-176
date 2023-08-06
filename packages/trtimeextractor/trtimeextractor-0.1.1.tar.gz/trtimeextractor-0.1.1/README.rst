The project was developed by `WesterOps`_. The goal of the project is
to develop a library to find and extract time/date information from
textual documents.

Why Should I Use This?
----------------------

The main goal is to identify texts fragments that are related to
time/date/period (exact date, time of day, day of the week, months,
seasons, time intervals, etc.) and make structural forms from them. We
tried to detect a variety of textual representations and handle things
like recurring times (e.g. “every Wednesday”).


Usage
-----

To use it, simply do:

::

    >>> from trtimeextractor import ExtractionService
    >>> text = "ikinci aralık"
    >>> ExtractionService.extract(text)

A ``PySettings`` can be applied to specify some additional extraction
options, like setting local user date/time, time-zone offset, filtering
extraction rules and finding latest dates.

``PySettingsBuilder`` is used for constructing ``PySettings`` instance
when you need to set configuration options other than the default.
``PySettingsBuilder`` is best used by creating it, and then invoking its
various configuration methods, and finally calling build method.

::

    >>> from trtimeextractor import PySettingsBuilder
    >>> settings = (PySettingsBuilder()
    ...          .addRulesGroup('DateGroup')
    ...          .excludeRules("relativeDateRule")
    ...          .addUserDate("2017-10-23T18:40:40.931Z")
    ...          .addTimeZoneOffset("2")
    ...          .includeOnlyLatestDates(True)
    ...          .build()
    ...         )
    >>> ExtractionService.extract(text, settings)

.. _WesterOps: https://www.westerops.com/
