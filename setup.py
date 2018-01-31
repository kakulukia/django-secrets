#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages


def get_version(*file_paths):
    """Retrieves the version from django_undeletable/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_secrets", "__init__.py")
readme = open('README.rst').read()
url = 'https://github.com/kakulukia/django-secrets'

setup(
    name='django-secrets',
    description='The easy way of handling Django secrets.',
    long_description=readme,
    version=version,
    author='Andy Grabow',
    author_email='andy@freilandkiwis.de',
    license='MIT',
    url=url,
    download_url=url + '/tarball/' + version,
    install_requires=[
        'Django>=1.11',
        'future',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['Django', 'secrets', 'deployment'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
    ],
)
