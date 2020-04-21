# Django Simple Category

> A simple django category libaray

This simple libaray provide an abstract Category class for django whitch does not need MPTT support.

## Feature overview

- Abstract Category class

## Install

## Usage

1. Add "simple-category" to your INSTALLED_APPS setting like this::

    ```python
    INSTALLED_APPS = [
        ...
        'simple-category',
    ]
    ```

2. Inherit from the Category class like this:

    ```python
    from simple_category.models import Category

    class MyCategory(Category):
        pass
    ```

3. Run `python manage.py migrate` to create your category models.
