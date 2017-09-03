# coding=utf-8
from setuptools import setup
from check_dlan_bandwidth import VERSION

setup(
    name='Check DLAN bandwidth',
    url='https://github.com/hoentschrode/check_dlan_bandwidth',
    version=VERSION,
    author='Christian Höntsch-Rode',
    author_email='hoentsch.rode@gmail.com',
    long_description=open('README.md').read(),
    keywords='devolo dlan python bandwidth',
    packages=['check_dlan_bandwidth', 'tests'],
    test_suite='tests',
    python_requires='>= 2.5, <3.0'
)
