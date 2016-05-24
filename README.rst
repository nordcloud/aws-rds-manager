.. image:: https://badge.fury.io/py/aws-rds-manager.svg
  :target: https://badge.fury.io/py/aws-rds-manager

.. image:: https://img.shields.io/pypi/pyversions/aws-rds-manager.svg
  :target: https://pypi.python.org/pypi/aws-rds-manager/1.0.2

.. image:: https://www.quantifiedcode.com/api/v1/project/d0e2098bfb494a17b26851c590681005/badge.svg
  :target: https://www.quantifiedcode.com/app/project/d0e2098bfb494a17b26851c590681005
  :alt: Code issues

.. image:: https://travis-ci.org/drewsonne/aws-rds-manager.svg?branch=master
  :target: https://travis-ci.org/drewsonne/aws-rds-manager

.. image:: https://codecov.io/gh/drewsonne/aws-rds-manager/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/drewsonne/aws-rds-manager

===============
aws-rds-manager
===============

Provides some utilities for the management of RDS snapshots

Installation
============
::

    pip install aws-rds-manager

Utilities
=========

aws-rds-snapshot-cleanup
------------------------
With a defined sunset period, removes instances based on a threshold to maintain a set number of snapshots.

Example
~~~~~~~
The following command will look for all snapshots created from the RDS database drew2,
and remove all snapshots leaving a minimum of 2. If less than 2 snapshots exist, then no
snapshots will be removed. ::

    aws-rds-snapshot-cleanup --sunset-period 2 --database-name drew2 \
            --profile myaccount --role arn:aws:iam::123456789012:role/RDSAccess \
            --region ap-southeast-2
