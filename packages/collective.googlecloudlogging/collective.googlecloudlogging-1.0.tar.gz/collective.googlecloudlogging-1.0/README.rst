=============================
collective.googlecloudlogging
=============================

This library connects to Python's standard logging module and will log to Googles Cloud Logging via API. More information at https://cloud.google.com/logging/docs/setup/python#connecting_the_library_to_python_logging

Configuration
-------------

- Within Google Cloud no extra configuration should be needed.
- If you want to use the Cloud Logging outside of Google Cloud, you have to supply your Google Cloud project ID and appropriate service account credentials.

Note
----

As soon as it's loaded, and only then, it will remove the StreamHandler from root logger and no longer write to stdout.
If you want no instance logging to stdout at all in your Google Cloud Logs, you have to disable it in your ``wsgi.ini``::


    [logger_root]
    level = INFO
    handlers = console, eventlog


Requirements
------------

* Plone 5.2
* Python 3.7


Installation
------------

Install collective.googlecloudlogging by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.googlecloudlogging


and then running ``bin/buildout``


Maintainers
-----------

- Peter Holzer

Contact: `dev@bluedynamics.com <mailto:dev@bluedynamics.com>`_


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.googlecloudlogging/issues
- Source Code: https://github.com/collective/collective.googlecloudlogging


License
-------

The project is licensed under the GPLv2.
