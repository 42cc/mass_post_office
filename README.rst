=======================
Django Mass Post Office
=======================

Django Post Office is a simple app to create emailing lists of users and sending
emails to them from admin. It depends on django-post-office (without "mass") so
please read it's documentation on how to send scheduled emails


Dependencies
============

* `django-post-office == 0.6.0 <https://github.com/ui/django-post_office>`_


Installation
============

* Currently no install from PyPI is available. so install with pip from github::

.. code-block:: bash

	pip install git+https://github.com/ui/django-post_office.git

* Add ``post_office`` and ``mass_post_office to your INSTALLED_APPS in django's ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        "post_office",
        "mass_post_office",
    )

* Run ``syncdb``::

    python manage.py syncdb

* Set ``post_office.EmailBackend`` as your ``EMAIL_BACKEND`` in django's ``settings.py``::

    EMAIL_BACKEND = 'post_office.EmailBackend'
