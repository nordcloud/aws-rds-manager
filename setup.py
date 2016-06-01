from setuptools import find_packages, setup

__version__ = '1.0.3'

setup(
    name='aws-rds-manager',
    description='CLI tool providing sunsetting of RDS snapshots',
    url='https://github.com/nordcloud/aws-rds-manager',
    long_description=open('README.rst').read(),
    version=__version__,
    packages=['awsrdsmanager'],
    download_url='https://github.com/nordcloud/aws-rds-manager/archive/v.{version}.tar.gz'.format(version=__version__),
    install_requires=['aws-auth-helper', 'six'],
    license='GPLv2',
    test_suite='tests',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    entry_points={
        'console_scripts': [
            'aws-rds-snapshot-cleanup=awsrdsmanager.__main__:sunset_rds_snapshots'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database',
        'Topic :: System :: Archiving :: Backup'
    ]

)
