#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('VERSION.txt', 'r') as v:
    version = v.read().strip()

with open('REQUIREMENTS.txt', 'r') as r:
    requires = r.read().split()

with open('README.rst', 'r') as r:
    readme = r.read()

download_url = (
    'https://github.com/juliomalegria/python-craigslist/tarball/%s'
)


setup(
    name='python-craigslist',
    packages=['craigslist'],
    version=version,
    description=('Simple Craigslist wrapper.'),
    long_description=readme,
    author='Julio M Alegria',
    author_email='juliomalegria@gmail.com',
    url='https://github.com/juliomalegria/python-craigslist',
    download_url=download_url % version,
    install_requires=requires,
    license='MIT-Zero'
)
