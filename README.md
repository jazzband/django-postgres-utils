# PostgreSQL lookups and functions for Django apps

[![Build Status](https://travis-ci.org/Canned-Django/django-postgres-utils.svg?branch=master)](https://travis-ci.org/Canned-Django/django-postgres-utils)
[![Documentation Status](https://readthedocs.org/projects/canned-djangodjango-postgres-utils/badge/?version=latest)](https://canned-djangodjango-postgres-utils.readthedocs.io/en/latest/?badge=latest)

How often have you had the impression that Django was not providing all the lookup expressions and
functions for your queries? Probably not that often, but now here is a **small** collection that I
consider quite useful.

## Installation

Just use:

```bash
pip install django-postgres-tweaks
```

As the title says it already, these tools are designed to be used in Django projects/apps. So make 
sure to add `postgres_utils` or `postgres_utils.apps.PostgresUtilsConfig` to the `INSTALLED_APPS` 
list in your project's `settings.py`!

That's it.

## Usage

### Lookups

The lookups provided by this package/app are automatically loaded when the app is installed. You
can go ahead and just use them like Django's built-in lookups, e.g.:

```python
Pizza.objects.filter(name__noregex="[ ]+")
```

Assume you have a model called ``Pizza`` with a ``name`` field.

### Functions

Like the DB functions provided by Django, e.g. in ``django.db.models.functions``, you need to need
to import them prior to usage. An example query looks like this:

```python
Topping.objects\
    .filter(name__contains="Onion")\
    .annotate(onion_color=RegexpReplace("name", " *Onion$", ""))\
    .values("name", "onion_color")\
    .order_by("name")
```
