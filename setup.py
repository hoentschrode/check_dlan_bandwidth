# coding=utf-8
from setuptools import setup, find_packages
from check_dlan_bandwidth import VERSION


setup(
    name='check_dlan_bandwidth',
    url='https://github.com/hoentschrode/check_dlan_bandwidth',
    version=VERSION,
    author='Christian Höntsch-Rode',
    author_email='hoentsch.rode@gmail.com',
    long_description=open('README.md').read(),
    keywords='devolo dlan python bandwidth',
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    python_requires='>= 2.5, <3.0',
    install_requires=[
        'nagiosplugin >= 1.2.4'
    ],
    entry_points={
        'console_scripts': [
            'check_dlan_bandwidth = check_dlan_bandwidth.check_dlan_bandwidth:main'
        ]
    }
)
