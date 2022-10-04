[![PyPI version](https://badge.fury.io/py/pip.svg)](https://badge.fury.io/py/pip)

# Django Simple Category

> A simple django category libaray

This simple libaray provide an abstract Category class for django whitch does not need MPTT support.

## Feature overview

- Abstract Category class

## Install

```shell
pip install django-simple-category
```

## Usage

1. Add "simple-category" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        'category',
    ]
    ```

2. Inherit from the Category class like this:

    ```python
    from simple_category.models import Category

    class MyCategory(Category):
        pass
    ```

3. Run migrations to create your category models.

    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```
