from __future__ import absolute_import, unicode_literals
from setuptools import setup, find_packages

setup(
    name='django-rest-framework-expandable',
    version='0.0.2',
    description='Mixins for DRF to allow expansion of fields.',
    long_description='',
    author='Olle Vidner',
    author_email='olle@vidner.se',
    url='https://github.com/ovidner/django-rest-framework-expandable',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'djangorestframework',
        'six'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ]
)
