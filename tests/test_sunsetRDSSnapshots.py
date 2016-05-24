from unittest import TestCase
from datetime import datetime
from awsrdsmanager.sunsetrdssnapshots import SunsetRDSSnapshots, NoSnapshotsError
from tests.helper import MockObject, MockMethod


class TestSunsetRDSSnapshots(TestCase):
    def setUp(self):
        self.maxDiff = None

    # def test__sort_snapshots_by_threshold_date(self):
    #     sunset_snapshot_command = SunsetRDSSnapshots(
    #         database_name='',
    #         sunset_period=5,
    #         region='',
    #         dry_run=True,
    #         session=None,
    #         enable_logging=False
    #     )
    #
    #     snapshots_before, snapshots_after = sunset_snapshot_command._sort_snapshots_by_threshold_date(
    #         threshold_date='',
    #         snapshots=[{
    #
    #         }]
    #     )

    def test_obj_list_sort(self):
        sunset_snapshot_command = SunsetRDSSnapshots(
            database_name='',
            sunset_period=5,
            region='',
            dry_run=True,
            session=None,
            enable_logging=False
        )
        result = sunset_snapshot_command._sort_by_key('SnapshotCreateTime', [{
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }])

        self.assertListEqual(result, [{
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }], )

    def test__sort_snapshots_by_threshold_period(self):
        sunset_snapshot_command = SunsetRDSSnapshots(
            database_name='',
            sunset_period=5,
            region='',
            dry_run=True,
            session=None,
            enable_logging=False
        )

        snapshots_before, snapshots_after = sunset_snapshot_command._sort_snapshots_by_threshold_period(
            threshold_count=2,
            snapshots=[{
                'SnapshotCreateTime': datetime(2015, 1, 1),
                'MasterUsername': 'first_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 2),
                'MasterUsername': 'second_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 3),
                'MasterUsername': 'third_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 4),
                'MasterUsername': 'fourth_entry'
            }]
        )

        self.assertListEqual(snapshots_before, [{
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }])

        self.assertListEqual(snapshots_after, [{
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }])

    def test__build_arg_parse(self):
        argparser = SunsetRDSSnapshots._build_arg_parse()
        namespace = argparser.parse_args(args=[
            '--database-name', 'test_db',
            '--sunset-period', '2',
            '--log-level', 'INFO',
            '--dry-run',
        ])

        self.assertEqual(namespace.database_name, 'test_db')
        self.assertEqual(namespace.sunset_period, 2)
        self.assertEqual(namespace.log_level, 'INFO')
        self.assertEqual(namespace.dry_run, True)

    def test_load(self):
        command_class = SunsetRDSSnapshots.load(args=[
            'aws-rds-snapshot-cleanup',
            '--database-name', 'test_db',
            '--sunset-period', '2',
            '--log-level', 'INFO',
            '--region', 'eu-west-1',
            '--dry-run',
        ])

        self.assertEqual(command_class.database_name, 'test_db')
        self.assertEqual(command_class.sunset_period, 2)
        self.assertEqual(command_class.logging_level, 'INFO')
        self.assertEqual(command_class.dry_run, True)
        self.assertEqual(command_class.region, 'eu-west-1')

    def test_NoSnapshotsError(self):
        try:
            raise NoSnapshotsError('hallo')
        except NoSnapshotsError as e:
            self.assertEqual(e.args[0], "No snapshots found for database 'hallo'")

    def test_run_no_snapshots(self):
        command_class = SunsetRDSSnapshots.load(args=[
            'aws-rds-snapshot-cleanup',
            '--database-name', 'test_db',
            '--sunset-period', '2',
            '--log-level', 'INFO',
            '--region', 'eu-west-1',
            '--dry-run',
        ])

        mock_rds_client = MockObject(
            describe_db_snapshots=MockMethod(response={'DBSnapshots': {}}),
            delete_db_snapshot=MockMethod()
        )

        command_class._get_rds_client = lambda region: mock_rds_client

        with self.assertRaises(NoSnapshotsError):
            command_class.run()

    def test_run_dryrun(self):
        command_class = SunsetRDSSnapshots.load(args=[
            'aws-rds-snapshot-cleanup',
            '--database-name', 'test_db',
            '--sunset-period', '2',
            '--log-level', 'INFO',
            '--region', 'eu-west-1',
            '--dry-run',
        ])

        mock_rds_client = MockObject(
            describe_db_snapshots=MockMethod(response={'DBSnapshots': [{
                'SnapshotCreateTime': datetime(2015, 1, 1),
                'MasterUsername': 'first_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 2),
                'MasterUsername': 'second_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 3),
                'MasterUsername': 'third_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 4),
                'MasterUsername': 'fourth_entry'
            }]}),
            delete_db_snapshot=MockMethod()
        )

        command_class._get_rds_client = lambda region: mock_rds_client

        response = command_class.run()

        self.assertListEqual(response['DeletedSnapshots'], [{
            'SnapshotCreateTime': datetime(2015, 1, 2),
            'MasterUsername': 'second_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 1),
            'MasterUsername': 'first_entry'
        }])

        self.assertListEqual(response['Snapshots'], [{
            'SnapshotCreateTime': datetime(2015, 1, 4),
            'MasterUsername': 'fourth_entry'
        }, {
            'SnapshotCreateTime': datetime(2015, 1, 3),
            'MasterUsername': 'third_entry'
        }])

    def test_run(self):
        command_class = SunsetRDSSnapshots.load(args=[
            'aws-rds-snapshot-cleanup',
            '--database-name', 'test_db',
            '--sunset-period', '2',
            '--log-level', 'INFO',
            '--region', 'eu-west-1'
        ])

        mock_rds_client = MockObject(
            describe_db_snapshots=MockMethod(response={'DBSnapshots': [{
                'SnapshotCreateTime': datetime(2015, 1, 1),
                'DBSnapshotIdentifier': 'first_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 2),
                'DBSnapshotIdentifier': 'second_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 3),
                'DBSnapshotIdentifier': 'third_entry'
            }, {
                'SnapshotCreateTime': datetime(2015, 1, 4),
                'DBSnapshotIdentifier': 'fourth_entry'
            }]}),
            delete_db_snapshot=MockMethod()
        )

        command_class._get_rds_client = lambda region: mock_rds_client

        command_class.run()

        self.assertEqual(
            mock_rds_client.delete_db_snapshot.calls[0].kwargs,
            {'DBSnapshotIdentifier': 'second_entry'}
        )
        self.assertEqual(
            mock_rds_client.delete_db_snapshot.calls[1].kwargs,
            {'DBSnapshotIdentifier': 'first_entry'}
        )

        self.assertEqual(
            mock_rds_client.describe_db_snapshots.calls[0].kwargs,
            {'SnapshotType': 'manual', 'DBInstanceIdentifier': 'test_db'}
        )
