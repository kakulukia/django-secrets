Keep your secrets secret!
=========================

This little app helps you to not commit your secrets to a repo and adds
a nice way of exporting/importing secrets for a new deployment.

Installation
------------

::

    pip install django-secrets

Usage
-----

After installing the package please add it to your ``INSTALLED_APPS``
setting

::

    INSTALLED_APPS = (
        ...
        'django_secrets',
    )

Because we want to be able to hide our secret settings, we have to alter
manage.py to run some code before the Django magic happens. Open
``manage.py`` and alter it like this:

::

    if __name__ == "__main__":

        from django_secrets.startup import check
        check()

        ...


Now that the check is in place, run ``manage.py`` to initialize your
project. This wll create a new secrets package in your project root with
the following contents:

::

    secrets
    ├── .gitignore
    ├── __init__.py
    ├── definitions.py
    └── secrets.py

The package also features a .gitignore file to prevent you from checking
in any secrets to git. Now open ``definitions.py`` to add your secrets
to the list. Start with the Django secret key for example. When your
done adding all secrets, run ``manage.py`` again and you wil be asked to
enter your secrets.

Now you can remove your secrets from ``settings.py`` and instead replace
them like this:

::

    from secrets import secrets

    SECRET_KEY = secrets.SECRET_KEY

Since the secrets are saved in a normal python package, you can just use
them the normal way, but now they are save! :)

Import / Export
---------------

This package adds a new managemant command: ``export_secrets``. This
will print out export statements so you can easily create environment
variables on a new machine and let the ``check`` function do the rest
for you, because it will also read in any known environment variables as
secret values.

Have fun and stay safe!
