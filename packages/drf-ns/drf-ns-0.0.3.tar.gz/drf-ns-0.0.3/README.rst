=================
Nested Serializer
=================


This is a Django Rest Framework addon to rezolve folowing problems
  - infinit level of nested serializer
  - different level of nested objects
  - writable nested objects

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "drf-ns" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'drf-ns',
    ]

2. This also includes ModelTracker as Base model class for your app

3. Run ``python manage.py migrate`` to create the models.
