aws-rds-manager
===============

Provides some utilities for the management of RDS snapshots

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
