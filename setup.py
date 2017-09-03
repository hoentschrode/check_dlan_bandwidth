# coding=utf-8
from setuptools import setup
from check_dlan_bandwidth import VERSION

setup(
    name='Check DLAN bandwidth',
    version=VERSION,
    author='Christian Höntsch-Rode',
    author_email='hoentsch.rode@gmail.com',
    long_description=open('README.md').read(),
    keywords='devolo dlan python bandwidth',
    py_modules=['check_dlan_bandwidth'],
    test_suite='tests',
    python_requires='>= 2.5, <=2.7'
)
