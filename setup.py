# @copyright: Andy Grabow (c) 2017. All rights reserved.

from setuptools import setup, find_packages
from pypandoc import convert_file

#: Converts the Markdown README in the RST format that PyPi expects.
long_description = convert_file('README.md', 'rst')

setup(
    name='django-secrets',
    description='The easy way of handling Django secrets.',
    long_description=long_description,
    version='0.2.0',
    url='https://github.com/kakulukia/django-secrets',
    download_url='https://github.com/kakulukia/django-secrets/tarball/0.2.0',
    author='Andy Grabow',
    author_email='andy@freilandkiwis.de',
    license='MIT',
    classifiers=[],
    install_requires=[
      'Django>=1.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['Django', 'secrets', 'deployment'],
)
