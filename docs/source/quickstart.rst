Quick Start
===========

Installation
------------

Just use:

.. code-block:: bash

   pip install django-postgres-utils

As the title says it already, these tools are designed to be used in Django projects/apps. So make
sure to add ``postgres_utils`` or ``postgres_utils.apps.PostgresUtilsConfig`` to the
``INSTALLED_APPS`` list in your project's ``settings.py``!

That's it.

Usage
-----

Lookups
^^^^^^^

The lookups provided by this package/app are automatically loaded when the app is installed. You
can go ahead and just use them like Django's built-in lookups, e.g.:

.. code-block:: python

   Pizza.objects.filter(name__noregex="[ ]+")

Assume you have a model called ``Pizza`` with a ``name`` field.

Functions
^^^^^^^^^

Like the DB functions provided by Django, e.g. in ``django.db.models.functions``, you need to need
to import them prior to usage. An example query looks like this:

.. code-block:: python

   Topping.objects\
      .filter(name__contains="Onion")\
      .annotate(onion_color=RegexpReplace("name", " *Onion$", ""))\
      .values("name", "onion_color")\
      .order_by("name")

