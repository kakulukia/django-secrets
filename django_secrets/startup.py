import io
import os

from six.moves import input
from six.moves import reload_module

from django_secrets.utils import green, red


def create_secrets_package(testing=False):
    try:
        os.stat('my_secrets')
    except Exception:
        os.mkdir('my_secrets')
    try:
        os.stat('my_secrets/__init__.py')
    except OSError:
        with io.open('my_secrets/__init__.py', 'w', encoding='utf8') as init_file:
            # just touch the file to create a new module
            init_file.close()

    with io.open('my_secrets/definitions.py', 'w', encoding='utf8') as definitions_file:
        definitions_file.write(u'# coding=utf-8\n\n')
        definitions_file.write(u'# Add your secrets to this list and run manage.py to set their values.\n')
        definitions_file.write(u'# Use them in settings.py like this:\n')
        definitions_file.write(u'# from secrets import secrets\n')
        definitions_file.write(u'# SECRET_KEY = secrets.SECRET_KEY\n\n')
        definitions_file.write(u'SECRET_KEYS = [\n')
        definitions_file.write(u'    # start with your Django secret key like this:\n')
        if testing:
            definitions_file.write(u'    "SECRET_KEY",\n')
            definitions_file.write(u'    "SECOND_SECRET",\n')
        else:
            definitions_file.write(u'    "SECRET_KEY",\n')
        definitions_file.write(u']\n')

    # test for ignore file and create it if needed
    if not os.path.isfile('my_secrets/.gitignore'):
        with io.open('my_secrets/.gitignore', 'w', encoding='utf8') as ignore_file:
            ignore_file.write(u'secrets.py\n')

    print(green('\nSecret definitions initialized under my_secrets/definitions.py'))
    print('Add your secrets there and fill the values on the next use of a manage.py command.\n\n')


def load_definitions():
    try:  # to load the secrets definitions for this project
        from my_secrets import definitions
    except ImportError:
        # .. otherwise initialize a new secrets package
        create_secrets_package()
        import my_secrets
        reload_module(my_secrets)
        from my_secrets import definitions

    reload_module(definitions)

    return definitions.SECRET_KEYS


def check():

    SECRET_KEYS = load_definitions()

    try:  # to import the existing secrets
        from my_secrets import secrets
    except ImportError:
        secrets = None

    # Configure the project with all secrets found in the definitions list
    # environment vars will be used if available
    filled_blanks = {}
    existing_data = {}
    intro_done = False

    for key in SECRET_KEYS:
        if secrets and hasattr(secrets, key) and getattr(secrets, key):
            existing_data[key] = getattr(secrets, key)
            continue  # for known secrets

        # otherwise try to get it from the environment or the user
        secret = os.environ.get(key)
        if secret:
            if not (secrets and hasattr(secrets, key)):
                print(green('got secret from environment variable (%s)' % key))
            filled_blanks[key] = secret
        else:  # pragma: no cover / inputs ain't possible in the CI
            if not intro_done:
                print(red('\nSecret missing, please fill in the blanks ..\n'))
                intro_done = True

            data = input(key + ': ')
            filled_blanks[key] = data

    if filled_blanks:  # in case of new data write the secrets file again
        secrets_file = 'my_secrets/secrets.py'
        if not os.path.exists(secrets_file):
            import sys
            from pathlib import Path
            app_path = Path(sys.argv[0]).parent
            secrets_file = str(app_path / secrets_file)

        with io.open(secrets_file, 'w', encoding='utf8') as secret_file:
            secret_file.write(u'#  coding=utf-8\n\n')
            for key, value in existing_data.items():
                secret_file.write(u'%s = "%s"\n' % (key, value))
            for key, value in filled_blanks.items():
                secret_file.write(u'%s = "%s"\n' % (key, value))

        # refresh the import system in case of new secrets or we just created the secrets package
        try:
            import my_secrets
            reload_module(my_secrets)
            from my_secrets import secrets
            reload_module(secrets)
        except ImportError:  # pragma: no cover
            # fixing travis import errors
            import importlib.util
            import sys
            spec = importlib.util.spec_from_file_location('secrets', 'my_secrets/secrets.py')
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            sys.modules['secrets'] = secrets

            spec = importlib.util.spec_from_file_location('my_secrets', 'my_secrets/__init__.py')
            my_secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(my_secrets)
            sys.modules['my_secrets'] = my_secrets
        except AttributeError:  # pragma: no cover / also just happening in travis
            pass
            # print(my_secrets)
            # print(secrets)
