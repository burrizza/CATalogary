#!/usr/bin/env python
####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
from setuptools import setup, find_packages

with open('README.md') as f_readme:
    long_description = f_readme.read()

with open('VERSION') as f_version:
    version = f_version.read()

setup(
    name='catalogary',
    description='CATalog(ary) - An open REST APIs and Web Scraping Wrapper',
    long_description=long_description,
    license='Apache License 2.0',
    version=version,
    packages=find_packages(include=['catalogary.api']),
    package_dir={"catalogary.api": "catalogary/api"},
    include_package_data=True,
    download_url='https://github.com/burrizza/CATalogary/releases',
    author='burrizza',
    author_email='',
    maintainer='burrizza',
    maintainer_email='',
    url='https://github.com/burrizza/CATalogary',
    install_requires=['requests', 'jsonschema'],
    platforms='Platform Independent',
    keywords=['CATalog', 'REST API', 'Open APIs', 'Bundesrepublik Deutschland', 'NINA', 'KATwarn', 'MoWaS', 'BIWapp', 'LHP', 'DWD', 'POLICE', 'Air Data', 'Bevoelkerungsschutz', 'Umweltbundesamt'],
    classifiers=[
        'Development Status :: Pre-Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)