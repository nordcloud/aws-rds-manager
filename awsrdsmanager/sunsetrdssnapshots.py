import argparse
import awsauthhelper

from awsrdsmanager.base import Base


class SunsetRDSSnapshots(Base):
    """
    Control the number of snapshots for an RDS database to be retained.
    """

    @classmethod
    def load(cls, args):
        """
        Parse cli arguments, and initialise the command

        :param List[str] args: List of cli args
        :return awsrdsmanager.SunsetRDSSnapshots:
        """

        awsargparser = cls._build_arg_parse()
        cli_options = awsargparser.parse_args(args=args[1:])

        # Perform authentication
        credentials = awsauthhelper.Credentials(**vars(cli_options))
        if credentials.has_role():
            credentials.assume_role()

        # Create a class
        return cls(
            database_name=cli_options.database_name,
            sunset_period=cli_options.sunset_period,
            dry_run=cli_options.dry_run,
            region=cli_options.region,
            logging_level=cli_options.log_level,
            session=credentials.create_session()
        )

    @classmethod
    def _build_arg_parse(cls):
        """
        Build the argument parser and return it

        :return:
        """
        argparser = argparse.ArgumentParser()
        argparser.add_argument('--database-name', help='Name of the database snapshot.', required=True)
        argparser.add_argument('--sunset-period', help='Number of snapshots to retains.', required=True, type=int)
        argparser.add_argument('--dry-run', help='Show snapshots to be deleted without deleting them',
                               action='store_true', default=False)

        cls._add_logging_options(argparser)

        awsargparser = awsauthhelper.AWSArgumentParser(role_session_name='register-instance', region='us-east-1',
                                                       parents=[argparser])
        return awsargparser

    def __init__(self, database_name, sunset_period, region, session, logging_level='INFO', enable_logging=True,
                 dry_run=False):
        """
        Set the region, session, and the database_name to operate on

        :param str database_name: Name of the database
        :param int sunset_period: How many snapshots to keep
        :param string region: Region to run this utility in
        :param callable(region=...) session: Function to return a botocore.Session object, with an optional region.
        :param string logging_level: Logging level
        :param bool enable_logging: True if logging should be enabled, and false if logging should be disabled.
        :param bool dry_run: True if no actions should be taken.
        :return:
        """
        super(SunsetRDSSnapshots, self).__init__(
            logging_level=logging_level,
            dry_run=dry_run,
            enable_logging=enable_logging
        )
        self.database_name = database_name
        self.sunset_period = sunset_period
        self.region = region
        self.session = session

    def run(self):
        """
        Remove any snapshots for the provided database_name which have more than the allowed number of snapshots.

        :return Dict[str, Dict[str, str]]:
        """

        self.rds_client = self._get_rds_client(region=self.region)

        snapshot_response = self.rds_client.describe_db_snapshots(
            DBInstanceIdentifier=self.database_name,
            SnapshotType='manual'
        )

        self.logger.debug('Snapshots : {0}'.format(
            snapshot_response['DBSnapshots']
        ))

        if not snapshot_response['DBSnapshots']:
            raise NoSnapshotsError(self.database_name)

        remaining_snapshots, deprecated_snapshots = self._sort_snapshots_by_threshold_period(
            self.sunset_period,
            snapshot_response['DBSnapshots']
        )

        if not self.dry_run:
            for snapshot in deprecated_snapshots:
                self.rds_client.delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])

        return {
            'Snapshots': remaining_snapshots,
            'DeletedSnapshots': deprecated_snapshots
        }

    def _get_rds_client(self, region):
        """
        Return a boto3.rds client object

        :return:
        """
        return self.session(region=region).client('rds')

    def _sort_snapshots_by_threshold_period(self, threshold_count, snapshots):
        """
        Return 2 lists where the first is snapshots after the threshold, and the second is snapshots after the threshold

        :param Dict[str, str|int|datetime|bool] snapshots:
        :param int threshold_count: maximum number of snapshots to be returned in snapshots_after.
        :return snapshots_before, snapshots_after:
        """

        snapshots = filter(lambda snapshot: 'SnapshotCreateTime' in snapshot, snapshots)

        sorted_snapshots = self._sort_by_key('SnapshotCreateTime', snapshots)

        return sorted_snapshots[:threshold_count], sorted_snapshots[threshold_count:]

    @staticmethod
    def _sort_by_key(key, dict_list):
        """
        Sort a list of dictionaries by a key

        :param str|int key: Key to sort list by
        :param List[Dict[str|int, object]] dict_list: List of dictionaries to sort
        :return List[Dict[str|int, object]]: Sorted List of dictionaries
        """

        def sorter_callback(item):
            return item[key]

        return sorted(dict_list, key=sorter_callback, reverse=True)


class NoSnapshotsError(Exception):
    """
    Exception thrown if no snapshots are found
    """

    def __init__(self, database_name):
        super(NoSnapshotsError, self).__init__(
            "No snapshots found for database \'{name}\'".format(name=database_name)
        )
