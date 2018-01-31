import os
import shutil

from django.test import TestCase

from django_secrets.startup import check, create_secrets_package


class SecretTest(TestCase):

    def test_adding_a_secret(self):
        self.assertEqual(True, True)

    def test_creating_secrets_folder(self):

        self.assertIn('secrets', os.listdir('.'))
        shutil.rmtree("secrets")
        self.assertNotIn('secrets', os.listdir('.'))
        create_secrets_package(testing=True)
        self.assertIn('secrets', os.listdir('.'))

        # test adding back the secret
        os.environ["SECOND_SECRET"] = "blub"
        check()
        from secrets import secrets
        self.assertEqual(secrets.SECOND_SECRET, 'blub')

    def test_export(self):
        from django_secrets.management.commands.export_secrets import Command

        command = Command()
        command.handle()
