# coding=utf-8
from setuptools import setup, find_packages
import distutils.cmd
import distutils.log
import subprocess
from check_dlan_bandwidth import VERSION


class UpdateIcingaExchangeCmd(distutils.cmd.Command):
    """
    Custom command to generate icinga exchange configuration
    """

    description = 'Update configuration for icingaexchange.yml'
    user_options = [
        # The format is (long option, short option, description).
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pystache

        command = ['/usr/bin/md5sum', 'check_dlan_bandwidth/check_dlan_bandwidth.py']
        self.announce('Running command: {}'.format(str(command)), level=distutils.log.INFO)
        output = subprocess.check_output(command)
        checksum = output.split(' ')[0]

        config_filename = 'icingaexchange.yml'
        self.announce('Generating icinga exchange configuration: {}'.format(config_filename), level=distutils.log.INFO)
        config = pystache.render(
            open('icingaexchange.yml.mustache').read(),
            {
                'version': VERSION,
                'md5_checksum': checksum
            })
        with open(config_filename, 'w') as fp:
            fp.write(config)

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
    extras_require={
        'dev': [
            'pystache >= 0.5.4'
        ]
    },
    entry_points={
        'console_scripts': [
            'check_dlan_bandwidth = check_dlan_bandwidth.check_dlan_bandwidth:main'
        ]
    },
    cmdclass={
        'update_icingaexchange': UpdateIcingaExchangeCmd
    }
)
