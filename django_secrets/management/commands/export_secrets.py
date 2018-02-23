from django.core.management.base import BaseCommand

from django_secrets.utils import green
from my_secrets import definitions


class Command(BaseCommand):
    help = 'Configures the project to use all the latest an greatest secrets.'

    def handle(self, *args, **options):

        from my_secrets import secrets
        print(green('\nUse these lines to initialize your secrets ..\n'))
        for key in definitions.SECRET_KEYS:
            print('export %s="%s"' % (key, getattr(secrets, key)))
        print('\n\n')
