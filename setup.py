# @copyright: Andy Grabow (c) 2017. All rights reserved.
import io
from setuptools import setup, find_packages

setup(
    name='django-secrets',
    description='The easy way of handling Django secrets.',
    version='0.2.1',
    url='https://github.com/kakulukia/django-secrets',
    download_url='https://github.com/kakulukia/django-secrets/tarball/0.2.1',
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
