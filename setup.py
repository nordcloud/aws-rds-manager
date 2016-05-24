from distutils.core import setup

setup(
    name='aws-rds-manager',
    version='1.0.0',
    packages=['awsrdsmanager'],
    install_requires=['aws-auth-helper'],
    url='',
    license='GPLv2',
    author='Drew J. Sonne',
    author_email='drew.sonne@nordcloud.com',
    description='',
    entry_points={
        'console_scripts': [
            'aws-rds-snapshot-cleanup=awsrdsmanager.__main__:sunset_rds_snapshots'
        ]
    }
)
