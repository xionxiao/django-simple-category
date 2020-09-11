======================
Django Simple Category
======================

A simple django category libaray

This simple libaray provide an abstract Category class for django whitch does not need MPTT support.

Feature overview
----------------

Abstract Category class

Install
-------

::

    $ pip install django-simple_category

Usage
-----

1. Add "simple-category" to your INSTALLED_APPS setting like this::

.. code:: python

    INSTALLED_APPS = [
        'category',
    ]


2. Inherit from the Category class like this::

.. code:: python

    from simple_category.models import Category

    class MyCategory(Category):
        pass


3. Run migrations::

::

    $ python manage.py migrate
