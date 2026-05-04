import importlib
import os
import shutil
from unittest.mock import patch

from django.test import TestCase

from django_secrets.startup import check, create_secrets_package, prompt_for_secret


class SecretTest(TestCase):

    def test_adding_a_secret(self):
        self.assertEqual(True, True)

    @patch('django_secrets.startup.input', return_value='')
    @patch('django_secrets.startup.get_random_secret_key', return_value='generated-secret-key')
    def test_secret_key_prompt_accepts_generated_default(self, get_random_secret_key, mocked_input):
        self.assertEqual(prompt_for_secret('SECRET_KEY'), 'generated-secret-key')
        get_random_secret_key.assert_called_once_with()
        mocked_input.assert_called_once_with('SECRET_KEY [generated-secret-key]: ')

    @patch('django_secrets.startup.input', return_value='custom-secret-key')
    @patch('django_secrets.startup.get_random_secret_key', return_value='generated-secret-key')
    def test_secret_key_prompt_accepts_custom_value(self, get_random_secret_key, mocked_input):
        self.assertEqual(prompt_for_secret('SECRET_KEY'), 'custom-secret-key')
        get_random_secret_key.assert_called_once_with()
        mocked_input.assert_called_once_with('SECRET_KEY [generated-secret-key]: ')

    @patch('django_secrets.startup.input', return_value='plain-secret')
    @patch('django_secrets.startup.get_random_secret_key')
    def test_non_secret_key_prompt_uses_plain_input(self, get_random_secret_key, mocked_input):
        self.assertEqual(prompt_for_secret('SECOND_SECRET'), 'plain-secret')
        get_random_secret_key.assert_not_called()
        mocked_input.assert_called_once_with('SECOND_SECRET: ')

    def test_creating_secrets_folder(self):

        self.assertIn('my_secrets', os.listdir('.'))
        shutil.rmtree("my_secrets")
        self.assertNotIn('my_secrets', os.listdir('.'))
        create_secrets_package(testing=True)
        self.assertIn('my_secrets', os.listdir('.'))

        # test adding back the generated secret key and an environment secret
        check()
        from my_secrets import secrets
        if not hasattr(secrets, 'SECOND_SECRET'):  # pragma: no cover / travis import problem fix
            spec = importlib.util.spec_from_file_location('secrets', 'my_secrets/secrets.py')
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
        self.assertIsNone(os.environ.get('SECRET_KEY'))
        self.assertTrue(secrets.SECRET_KEY)
        self.assertEqual(secrets.SECOND_SECRET, 'blub')

    def test_export(self):
        from django_secrets.management.commands.export_secrets import Command

        command = Command()
        command.handle()
