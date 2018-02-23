import importlib

from django.core.management.base import BaseCommand

from django_secrets.utils import green
from my_secrets import definitions


class Command(BaseCommand):
    help = 'Configures the project to use all the latest an greatest secrets.'

    def handle(self, *args, **options):

        from my_secrets import secrets

        # travis test fixes
        for key in definitions.SECRET_KEYS:
            if not hasattr(secrets, key):  # pragma: no cover travis problems
                spec = importlib.util.spec_from_file_location('secrets', 'my_secrets/secrets.py')
                secrets = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(secrets)
                break

        print(green('\nUse these lines to initialize your secrets ..\n'))
        for key in definitions.SECRET_KEYS:
            print('export %s="%s"' % (key, getattr(secrets, key)))
        print('\n\n')
