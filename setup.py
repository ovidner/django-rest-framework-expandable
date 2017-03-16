from __future__ import absolute_import, unicode_literals
from setuptools import setup

setup(
    name='djangorestframework-expandable',
    version='0.0.6',
    description='Mixins for DRF to allow expansion of fields.',
    author='Olle Vidner',
    author_email='olle@vidner.se',
    url='https://github.com/ovidner/django-rest-framework-expandable',
    packages=[
        'rest_framework_expandable'
    ],
    install_requires=[
        'Django',
        'djangorestframework',
        'six'
    ]
)
