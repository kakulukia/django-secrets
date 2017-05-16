import io
import os

from builtins import input
from imp import reload

from django_secrets.utils import green, red

try:  # to load the secrets definitions for this project
    from secrets.definitions import SECRET_KEYS
except ImportError:

    # .. otherwise initialize a new secrets package
    print(green('\nSecret definitions initialized under secrets/definitions.py'))
    print('Add your secrets there and fill the values on the next use of a manage.py command.\n\n')

    try:
        os.stat('secrets')
    except:
        os.mkdir('secrets')
        with io.open('secrets/__init__.py', 'w', encoding='utf8') as init_file:
            # just touch the file to create a new module
            pass

    with io.open('secrets/definitions.py', 'w', encoding='utf8') as definitions_file:
        definitions_file.write(u'# coding=utf-8\n\n')
        definitions_file.write(u'# Add your secrets to this list and run manage.py to set their values.\n')
        definitions_file.write(u'# Use them in settings.py like this:\n')
        definitions_file.write(u'# from secrets import secrets\n')
        definitions_file.write(u'# SECRET_KEY = secrets.SECRET_KEY\n\n')
        definitions_file.write(u'SECRET_KEYS = [\n')
        definitions_file.write(u'    # start with your Django secret key like this:\n')
        definitions_file.write(u'    # "SECRET_KEY",\n')
        definitions_file.write(u']\n')

    SECRET_KEYS = []

def check():
    try:  # to import the existing secrets
        from secrets import secrets
    except ImportError:
        secrets = None

        # test for ignore file and create it if needed
        if not os.path.isfile('secrets/.gitignore'):
            with io.open('secrets/.gitignore', 'w', encoding='utf8') as ignore_file:
                ignore_file.write(u'secrets.py\n')

    # Configure the project with all secrets found in the definitions list
    # environment vars will be used as values if available
    filled_blanks = {}
    intro_done = False

    for key in SECRET_KEYS:

        secret = (secrets and hasattr(secrets, key) and getattr(secrets, key)) or os.environ.get(key)
        if secret:
            if not (secrets and hasattr(secrets, key)):
                print(green('got secret from environment variable (%s)' % key))
            filled_blanks[key] = secret
        else:

            if not intro_done:
                print(red('\nSecret missing, please fill in the blanks ..\n'))
                intro_done = True

            data = input(key + ': ')
            filled_blanks[key] = data

    with io.open('secrets/secrets.py', 'w', encoding='utf8') as secret_file:

        secret_file.write(u'#  coding=utf-8\n\n')
        for key, value in filled_blanks.items():
            secret_file.write(u'%s = "%s"\n' % (key, value))

    # maybe we had a new value added so refresh the import system
    if secrets:
        reload(secrets)
