# @copyright: Andy Grabow (c) 2017. All rights reserved.
import io
from setuptools import setup, find_packages

setup(
    name='django-secrets',
    description='The easy way of handling Django secrets.',
    version='0.2.4',
    url='https://github.com/kakulukia/django-secrets',
    download_url='https://github.com/kakulukia/django-secrets/tarball/0.2.4',
    author='Andy Grabow',
    author_email='andy@freilandkiwis.de',
    license='MIT',
    install_requires=[
      'Django>=1.8',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
    ],
)
