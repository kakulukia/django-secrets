import io
import os

from os.path import expanduser

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from secrets import definitions

from django_secrets.utils import green

try:
    from secrets.definitions import SECRET_KEYS
except ImportError, e:
    print('\n\nPlease configure your secret definitions inside <project root>/secrets/definitions.py\n\n')
    exit()

class Command(BaseCommand):
    help = 'Configures the project to use all the latest an greatest secrets.'

    def handle(self, *args, **options):

        from secrets import secrets
        print(green('\nUse these lines to initialize your secrets ..\n'))
        for key in definitions.SECRET_KEYS:
            print('export %s="%s"' % (key, getattr(secrets, key)))
        print('\n\n')
