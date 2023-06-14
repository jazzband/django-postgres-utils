#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def get_requires():
    def _filter(requires):
        return [req.strip() for req in requires if req.strip()]

    filename = "requirements.txt"

    with open(filename, "r") as fh:
        return _filter(fh.readlines())


with open("README.md") as fh:
    long_description = fh.read()


setup(
    name='django-postgres-tweaks',
    version='0.1.4',
    description='Special PostgreSQL lookups and functions for Django apps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Andreas Hasenkopf',
    author_email='andreas@hasenkopf.xyz',
    url='https://github.com/jazzband/django-postgres-utils',
    project_urls={
        'Documentation': 'https://canned-djangodjango-postgres-utils.readthedocs.io/'
    },
    packages=["postgres_utils"],
    package_dir={'': 'src'},
    license='MIT',
    install_requires=get_requires(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database"
    ]
)
